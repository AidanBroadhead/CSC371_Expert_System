import streamlit as st



# ============================================================
# Job Qualification Expert System
# ============================================================
# This expert system evaluates an applicant against the
# requirements listed for four available positions.
#
# "Needed Skills" and "Qualifications" are treated as
# required requirements.
# "Desired Skills" are not required for qualification.
# ============================================================


def get_years(value, field_name):
    """
    Validate years of experience.
    Input must be a whole number from 0 to 99.
    """
    try:
        years = int(value)
    except (ValueError, TypeError):
        raise ValueError(
            f"{field_name} must be a whole number from 0 to 99."
        )

    # Reject decimal-looking inputs such as "2.5", and enforce the range.
    if str(years) != value.strip() or years < 0 or years > 99:
        raise ValueError(
            f"{field_name} must be a whole number from 0 to 99."
        )

    return years

def meets_degree_requirement(applicant_degree, required_degree):
    """
    Determine whether an applicant's degree satisfies a position's
    minimum degree requirement.

    A Masters in CS is considered to include the Bachelor's-level
    qualification, so a Master's applicant also satisfies a
    Bachelor in CS requirement.
    """
    degree_levels = {
        "Other": 0,
        "Bachelor in CS": 1,
        "Masters in CS": 2
    }

    return degree_levels.get(applicant_degree, 0) >= degree_levels[required_degree]


def evaluate_applicant(applicant):
    """
    Evaluate the applicant against each position.

    Returns:
        qualified: list of qualified position names
        not_qualified: dictionary mapping each unqualified
                       position to a list of reasons
    """

    qualified = []
    not_qualified = {}

    # --------------------------------------------------------
    # 1. Entry-Level Python Engineer
    #
    # Required:
    #   - Python coursework
    #   - Software Engineering coursework
    #   - Bachelor in CS
    #
    # Desired:
    #   - Agile course
    # --------------------------------------------------------
    reasons = []

    if not applicant["python_coursework"]:
        reasons.append("Python coursework is required.")

    if not applicant["software_engineering_coursework"]:
        reasons.append("Software Engineering coursework is required.")

    if not meets_degree_requirement(
        applicant["degree"],
        "Bachelor in CS"
    ):
        reasons.append("A Bachelor in CS is required.")

    if reasons:
        not_qualified["Entry-Level Python Engineer"] = reasons
    else:
        qualified.append("Entry-Level Python Engineer")

    # --------------------------------------------------------
    # 2. Python Engineer
    #
    # Required:
    #   - 3 years Python development
    #   - 1 year data development
    #   - Experience in Agile projects
    #   - Bachelor in CS
    #
    # Desired:
    #   - Used Git
    # --------------------------------------------------------
    reasons = []

    if applicant["python_years"] < 3:
        reasons.append(
            f"Requires at least 3 years of Python development; "
            f"applicant has {applicant['python_years']:g}."
        )

    if applicant["data_years"] < 1:
        reasons.append(
            f"Requires at least 1 year of data development; "
            f"applicant has {applicant['data_years']:g}."
        )

    if applicant["agile_years"] <= 0:
        reasons.append(
            "Experience in Agile projects is required."
        )

    if not meets_degree_requirement(
        applicant["degree"],
        "Bachelor in CS"
    ):
        reasons.append("A Bachelor in CS is required.")

    if reasons:
        not_qualified["Python Engineer"] = reasons
    else:
        qualified.append("Python Engineer")

    # --------------------------------------------------------
    # 3. Project Manager
    #
    # Required:
    #   - 3 years managing software projects
    #   - 2 years Agile projects
    #   - PMI Lean Project Management Certification
    #
    # No degree requirement is listed.
    # --------------------------------------------------------
    reasons = []

    if applicant["project_management_years"] < 3:
        reasons.append(
            f"Requires at least 3 years managing software projects; "
            f"applicant has {applicant['project_management_years']:g}."
        )

    if applicant["agile_years"] < 2:
        reasons.append(
            f"Requires at least 2 years of Agile project experience; "
            f"applicant has {applicant['agile_years']:g}."
        )

    if not applicant["pmi_certification"]:
        reasons.append(
            "PMI Lean Project Management Certification is required."
        )

    if reasons:
        not_qualified["Project Manager"] = reasons
    else:
        qualified.append("Project Manager")

    # --------------------------------------------------------
    # 4. Senior Knowledge Engineer
    #
    # Required:
    #   - 4 years Python development
    #   - 2 years Expert Systems development
    #   - 2 years data architecture/data development
    #   - Masters in CS
    # --------------------------------------------------------
    reasons = []

    if applicant["python_years"] < 4:
        reasons.append(
            f"Requires at least 4 years of Python development; "
            f"applicant has {applicant['python_years']:g}."
        )

    if applicant["expert_system_years"] < 2:
        reasons.append(
            f"Requires at least 2 years developing Expert Systems; "
            f"applicant has {applicant['expert_system_years']:g}."
        )

    if applicant["data_architecture_years"] < 2:
        reasons.append(
            f"Requires at least 2 years of data architecture/data "
            f"development; applicant has "
            f"{applicant['data_architecture_years']:g}."
        )

    if not meets_degree_requirement(
        applicant["degree"],
        "Masters in CS"
    ):
        reasons.append("A Masters in CS is required.")

    if reasons:
        not_qualified["Senior Knowledge Engineer"] = reasons
    else:
        qualified.append("Senior Knowledge Engineer")

    return qualified, not_qualified




st.set_page_config(page_title="Job Qualification Expert System", page_icon="💼")
st.title("Job Qualification Expert System")
st.write("Enter the applicant's information below. The system will determine which positions the applicant qualifies for and explain any disqualifying conditions.")

with st.form("applicant_form"):
    st.subheader("Education")
    degree = st.selectbox("Highest degree", ["Other", "Bachelor in CS", "Masters in CS"])

    st.subheader("Experience")
    col1, col2 = st.columns(2)
    with col1:
        python_years = st.number_input("Python development (years)", 0, 99, 0, 1)
        data_years = st.number_input("Data development (years)", 0, 99, 0, 1)
        agile_years = st.number_input("Agile project experience (years)", 0, 99, 0, 1)
    with col2:
        project_management_years = st.number_input("Software project management (years)", 0, 99, 0, 1)
        expert_system_years = st.number_input("Expert Systems development (years)", 0, 99, 0, 1)
        data_architecture_years = st.number_input("Data architecture/data development (years)", 0, 99, 0, 1)

    st.caption("Experience values must be whole numbers from 0 to 99.")

    st.subheader("Coursework")
    python_coursework = st.checkbox("Python coursework completed")
    software_engineering_coursework = st.checkbox("Software Engineering coursework completed")

    st.subheader("Other Qualifications")
    pmi_certification = st.checkbox("PMI Lean Project Management Certification")
    used_git = st.checkbox("Used Git")

    submitted = st.form_submit_button("Evaluate Applicant", type="primary", use_container_width=True)

if submitted:
    applicant = {
        "degree": degree,
        "python_years": int(python_years),
        "data_years": int(data_years),
        "agile_years": int(agile_years),
        "project_management_years": int(project_management_years),
        "expert_system_years": int(expert_system_years),
        "data_architecture_years": int(data_architecture_years),
        "python_coursework": python_coursework,
        "software_engineering_coursework": software_engineering_coursework,
        "pmi_certification": pmi_certification,
        "used_git": used_git,
    }

    qualified, not_qualified = evaluate_applicant(applicant)
    st.divider()
    st.header("Results")

    st.subheader("Qualified Positions")
    if qualified:
        for position in qualified:
            st.success(f"✓ {position} — All required qualifications are satisfied.")
    else:
        st.info("The applicant does not fully qualify for any available position.")

    st.subheader("Positions Not Qualified")
    if not_qualified:
        for position, reasons in not_qualified.items():
            with st.expander(f"✗ {position}", expanded=True):
                for reason in reasons:
                    st.write(f"• {reason}")
    else:
        st.success("The applicant meets the required qualifications for all available positions.")
