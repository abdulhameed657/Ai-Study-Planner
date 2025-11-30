# import streamlit as st
# import pandas as pd
# from datetime import datetime

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="AI Study Planner",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- Helper Functions ---

# def generate_schedule(subjects_df, availability):
#     """
#     Generates a study schedule based on subject difficulty and user availability.
#     This is the "AI" core of the app.
#     """
#     if subjects_df.empty or not availability:
#         return pd.DataFrame()

#     # 1. Prepare a list of study slots from availability
#     slots = []
#     for day, hours in availability.items():
#         if hours > 0:
#             slots.append({'day': day, 'duration': hours, 'assigned_subject': None})
    
#     # 2. Sort subjects by difficulty (hardest first) to prioritize them
#     #    We create a mutable list of subjects to track remaining hours
#     subjects_to_schedule = subjects_df.sort_values(by='Difficulty', ascending=False).to_dict('records')
#     for subject in subjects_to_schedule:
#         subject['remaining_hours'] = subject['Hours/Week']

#     # 3. Assign subjects to slots
#     #    We iterate through subjects and fill up the available day slots
#     for subject in subjects_to_schedule:
#         while subject['remaining_hours'] > 0:
#             # Find the next available day with the most free time (greedy approach)
#             best_slot = None
#             for slot in slots:
#                 if slot['assigned_subject'] is None:
#                     if best_slot is None or slot['duration'] > best_slot['duration']:
#                         best_slot = slot
            
#             if best_slot is None: # No more free slots
#                 break

#             # Assign hours to the best slot found
#             hours_to_assign = min(subject['remaining_hours'], best_slot['duration'])
            
#             # Update slot and subject
#             best_slot['assigned_subject'] = {
#                 'Subject': subject['Subject'],
#                 'Duration': hours_to_assign,
#                 'Difficulty': subject['Difficulty']
#             }
#             best_slot['duration'] -= hours_to_assign
#             subject['remaining_hours'] -= hours_to_assign

#     # 4. Format the final schedule into a DataFrame for display
#     schedule_list = []
#     for slot in slots:
#         if slot['assigned_subject']:
#             schedule_list.append({
#                 'Day': slot['day'],
#                 'Subject': slot['assigned_subject']['Subject'],
#                 'Duration (hrs)': slot['assigned_subject']['Duration'],
#                 'Difficulty': slot['assigned_subject']['Difficulty']
#             })
    
#     return pd.DataFrame(schedule_list)


# # --- Initialize Session State ---
# if 'subjects_df' not in st.session_state:
#     # Default data to make the app interactive on first run
#     st.session_state.subjects_df = pd.DataFrame([
#         {'Subject': 'Mathematics', 'Difficulty': 8, 'Hours/Week': 6},
#         {'Subject': 'English', 'Difficulty': 4, 'Hours/Week': 4},
#         {'Subject': 'Science', 'Difficulty': 2, 'Hours/Week': 2}
#     ])

# if 'availability' not in st.session_state:
#     st.session_state.availability = {
#         'Monday': 2.0, 'Tuesday': 1.5, 'Wednesday': 2.0, 'Thursday': 1.5,
#         'Friday': 3.0, 'Saturday': 4.0, 'Sunday': 1.0
#     }

# if 'schedule_df' not in st.session_state:
#     st.session_state.schedule_df = None


# # --- Sidebar for Inputs ---
# with st.sidebar:
#     st.header("⚙️ Planner Setup")

#     st.subheader("1. Add Your Subjects")
#     # Use st.data_editor for a clean, editable table interface
#     edited_subjects = st.data_editor(
#         st.session_state.subjects_df,
#         num_rows="dynamic",
#         use_container_width=True,
#         column_config={
#             "Subject": st.column_config.TextColumn(width="medium"),
#             "Difficulty": st.column_config.ProgressColumn(
#                 "Difficulty (1-10)",
#                 help="How difficult is this subject for you?",
#                 format="%.0f",
#                 min_value=1,
#                 max_value=10,
#             ),
#             "Hours/Week": st.column_config.NumberColumn(
#                 "Target Hours/Week",
#                 help="How many hours do you want to study this per week?",
#                 min_value=0.5,
#                 max_value=20.0,
#                 step=0.5,
#                 format="%.1f hrs"
#             )
#         },
#         hide_index=True,
#     )
#     st.session_state.subjects_df = edited_subjects

#     st.subheader("2. Set Your Availability")
#     availability = {}
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     for day in days:
#         availability[day] = st.slider(
#             f"{day}",
#             min_value=0.0,
#             max_value=8.0,
#             value=st.session_state.availability.get(day, 2.0),
#             step=0.5,
#             key=f"avail_{day}"
#         )
#     st.session_state.availability = availability
    
#     st.markdown("---")
    
#     # Button to trigger schedule generation
#     if st.button("🚀 Generate My Schedule", type="primary", use_container_width=True):
#         with st.spinner('Analyzing data and generating your personalized schedule...'):
#             st.session_state.schedule_df = generate_schedule(st.session_state.subjects_df, availability)
#             st.success("Schedule generated successfully!", icon="✅")
#             st.rerun() # Rerun to display the new schedule immediately

#     if st.button("🗑️ Clear Schedule", use_container_width=True):
#         st.session_state.schedule_df = None
#         st.rerun()


# # --- Main Page Layout ---
# st.title("🧠 AI Study Planner")
# st.markdown("Easily create a balanced and effective study plan. Add your subjects, set your availability, and let the AI do the rest.")

# # --- Display the Schedule ---
# if st.session_state.schedule_df is not None and not st.session_state.schedule_df.empty:
#     st.header("Your Generated Study Schedule")
    
#     # Display the main schedule table
#     st.dataframe(st.session_state.schedule_df, hide_index=True, use_container_width=True)

#     st.markdown("---")
    
#     col1, col2 = st.columns(2)

#     # --- Today's Focus (Reminder) ---
#     with col1:
#         st.subheader("🔔 Today's Focus")
#         today = datetime.now().strftime('%A')
#         todays_schedule = st.session_state.schedule_df[st.session_state.schedule_df['Day'] == today]
        
#         if not todays_schedule.empty:
#             for _, row in todays_schedule.iterrows():
#                 st.markdown(f"- **{row['Subject']}** ({row['Duration (hrs)']} hrs)")
#         else:
#             st.info("No study sessions scheduled for today. Enjoy your break!")

#     # --- Weekly Summary ---
#     with col2:
#         st.subheader("📊 Weekly Summary")
#         total_hours = st.session_state.schedule_df['Duration (hrs)'].sum()
#         st.metric("Total Study Hours This Week", f"{total_hours:.1f} hrs")
        
#         subject_hours = st.session_state.schedule_df.groupby('Subject')['Duration (hrs)'].sum()
#         st.write("**Hours per Subject:**")
#         st.bar_chart(subject_hours)

# else:
#     st.info("Configure your subjects and availability in the sidebar, then click 'Generate My Schedule' to begin.")




import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

# Configure the page
st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e86ab;
        margin: 1rem 0;
    }
    .subject-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
        color: #000000;
    }
    .day-schedule {
        background-color: #000000;
        color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .difficulty-easy { border-left: 4px solid #28a745; }
    .difficulty-medium { border-left: 4px solid #ffc107; }
    .difficulty-hard { border-left: 4px solid #dc3545; }
    .reminder {
        background-color: #fff3cd;
        color: #000000;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        border-left: 3px solid #ffc107;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

class AIStudyPlanner:
    def __init__(self):
        self.subjects = []
        self.schedule = {}
        self.difficulty_hours = {
            'Easy': 1,
            'Medium': 2,
            'Hard': 3
        }
    
    def add_subject(self, name, difficulty, priority, hours_per_week):
        """Add a subject to the planner with validation"""
        # Validate inputs
        if not name or not name.strip():
            raise ValueError("Subject name cannot be empty")
        
        if hours_per_week <= 0:
            raise ValueError("Hours per week must be positive")
        
        if priority < 1 or priority > 10:
            raise ValueError("Priority must be between 1 and 10")
        
        # Check for duplicate subject names
        existing_subjects = [s['name'].lower() for s in self.subjects]
        if name.lower() in existing_subjects:
            raise ValueError(f"Subject '{name}' already exists")
        
        subject = {
            'name': name.strip(),
            'difficulty': difficulty,
            'priority': priority,
            'hours_per_week': hours_per_week,
            'color': self._get_color_for_difficulty(difficulty),
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.subjects.append(subject)
        return True
    
    def edit_subject(self, old_name, new_name, difficulty, priority, hours_per_week):
        """Edit an existing subject"""
        for subject in self.subjects:
            if subject['name'] == old_name:
                subject['name'] = new_name
                subject['difficulty'] = difficulty
                subject['priority'] = priority
                subject['hours_per_week'] = hours_per_week
                subject['color'] = self._get_color_for_difficulty(difficulty)
                return True
        return False
    
    def delete_subject(self, subject_name):
        """Delete a subject from the planner"""
        self.subjects = [s for s in self.subjects if s['name'] != subject_name]
        return True
    
    def _get_color_for_difficulty(self, difficulty):
        """Get color based on difficulty level"""
        colors = {
            'Easy': '#28a745',
            'Medium': '#ffc107',
            'Hard': '#dc3545'
        }
        return colors.get(difficulty, '#6c757d')
    
    def generate_schedule(self, study_days, total_study_hours_per_day):
        """Generate an AI-powered study schedule"""
        self.schedule = {}
        
        # Initialize schedule
        for day in study_days:
            self.schedule[day] = {
                'subjects': [],
                'total_hours': 0,
                'available_hours': total_study_hours_per_day
            }
        
        # Sort subjects by priority (higher priority first)
        sorted_subjects = sorted(self.subjects, key=lambda x: x['priority'], reverse=True)
        
        # Distribute subjects across days
        for subject in sorted_subjects:
            hours_assigned = 0
            subject_hours_needed = subject['hours_per_week']
            
            while hours_assigned < subject_hours_needed:
                # Find day with most available hours
                best_day = None
                max_available = 0
                
                for day in study_days:
                    available = self.schedule[day]['available_hours']
                    if available > max_available:
                        max_available = available
                        best_day = day
                
                if best_day is None:
                    break
                
                # Assign hours to this day
                hours_to_assign = min(
                    self.difficulty_hours[subject['difficulty']],
                    self.schedule[best_day]['available_hours'],
                    subject_hours_needed - hours_assigned
                )
                
                if hours_to_assign > 0:
                    study_session = {
                        'subject': subject['name'],
                        'hours': hours_to_assign,
                        'difficulty': subject['difficulty'],
                        'color': subject['color']
                    }
                    
                    self.schedule[best_day]['subjects'].append(study_session)
                    self.schedule[best_day]['total_hours'] += hours_to_assign
                    self.schedule[best_day]['available_hours'] -= hours_to_assign
                    hours_assigned += hours_to_assign
                else:
                    break
    
    def get_study_tips(self, subject_name, difficulty):
        """Generate AI study tips based on subject and difficulty"""
        tips_library = {
            'Easy': [
                "Focus on understanding core concepts",
                "Create summary notes for quick revision",
                "Practice with simple exercises daily"
            ],
            'Medium': [
                "Break down complex topics into smaller parts",
                "Use spaced repetition for better retention",
                "Mix theory with practical applications"
            ],
            'Hard': [
                "Dedicate longer, uninterrupted study sessions",
                "Seek additional resources and explanations",
                "Form study groups for difficult concepts"
            ]
        }
        
        subject_specific_tips = {
            'Mathematics': ["Practice problems regularly", "Focus on understanding formulas"],
            'Physics': ["Relate concepts to real-world examples", "Practice derivations"],
            'Chemistry': ["Memorize key reactions", "Understand periodic trends"],
            'Biology': ["Create visual diagrams", "Use mnemonics for memorization"],
            'Programming': ["Code daily", "Work on small projects"],
            'History': ["Create timelines", "Connect events to causes and effects"],
            'Languages': ["Practice speaking daily", "Immerse yourself in the language"]
        }
        
        tips = tips_library.get(difficulty, [])
        
        # Add subject-specific tips
        for key, subject_tips in subject_specific_tips.items():
            if key.lower() in subject_name.lower():
                tips.extend(subject_tips)
                break
        
        return random.sample(tips, min(3, len(tips)))
    
    def generate_reminders(self):
        """Generate smart reminders for the study plan"""
        reminders = []
        
        # Check for overloaded days
        for day, plan in self.schedule.items():
            if plan['total_hours'] > 6:
                reminders.append(f"⚠️ {day} seems overloaded ({plan['total_hours']} hours). Consider redistributing.")
        
        # Check for difficult subjects
        hard_subjects = [s for s in self.subjects if s['difficulty'] == 'Hard']
        if len(hard_subjects) > 2:
            reminders.append("🎯 You have multiple difficult subjects. Consider spacing them out.")
        
        # General study tips
        reminders.extend([
            "📝 Take regular breaks (try Pomodoro technique: 25min study, 5min break)",
            "💧 Stay hydrated and maintain a healthy study environment",
            "🔁 Review previous topics regularly for better retention"
        ])
        
        return reminders

def add_subject_form():
    """Display the add subject form in sidebar"""
    st.markdown("---")
    st.subheader("📝 Add New Subject")
    
    with st.form("subject_form", clear_on_submit=True):
        # Subject name with validation
        subject_name = st.text_input(
            "Subject Name:",
            placeholder="e.g., Mathematics, Physics, Programming...",
            help="Enter the name of the subject you want to study"
        )
        
        # Difficulty level
        difficulty = st.selectbox(
            "Difficulty Level:",
            ['Easy', 'Medium', 'Hard'],
            help="Select how difficult this subject is for you"
        )
        
        # Priority with explanation
        priority = st.slider(
            "Priority (1-10):",
            1, 10, 5,
            help="1 = Lowest priority, 10 = Highest priority"
        )
        
        # Hours per week
        hours_per_week = st.slider(
            "Hours per week:",
            1, 20, 4,
            help="Total hours you want to dedicate to this subject per week"
        )
        
        # Form submission
        submitted = st.form_submit_button("➕ Add Subject", use_container_width=True)
        
        if submitted:
            if not subject_name or not subject_name.strip():
                st.error("❌ Please enter a subject name")
                return
            
            try:
                success = st.session_state.planner.add_subject(
                    subject_name.strip(), 
                    difficulty, 
                    priority, 
                    hours_per_week
                )
                if success:
                    st.markdown(
                        f'<div class="success-message">✅ Successfully added "{subject_name}"!</div>', 
                        unsafe_allow_html=True
                    )
                    st.rerun()
                    
            except ValueError as e:
                st.error(f"❌ {str(e)}")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

def manage_subjects_section():
    """Display section for managing existing subjects"""
    if st.session_state.planner.subjects:
        st.markdown("---")
        st.subheader("📋 Manage Subjects")
        
        # Display all subjects with edit/delete options
        for i, subject in enumerate(st.session_state.planner.subjects):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                difficulty_class = f"difficulty-{subject['difficulty'].lower()}"
                st.markdown(
                    f"""
                    <div class="subject-card {difficulty_class}">
                        <h4>{subject['name']}</h4>
                        <p><strong>Difficulty:</strong> {subject['difficulty']} | 
                        <strong>Priority:</strong> {subject['priority']}/10 | 
                        <strong>Hours/Week:</strong> {subject['hours_per_week']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                # Edit button
                if st.button("✏️ Edit", key=f"edit_{i}"):
                    st.session_state.editing_subject = subject['name']
            
            with col3:
                # Delete button with confirmation
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    st.session_state.deleting_subject = subject['name']
        
        # Handle subject editing
        if hasattr(st.session_state, 'editing_subject'):
            edit_subject_form(st.session_state.editing_subject)
        
        # Handle subject deletion
        if hasattr(st.session_state, 'deleting_subject'):
            delete_subject_confirmation(st.session_state.deleting_subject)

def edit_subject_form(subject_name):
    """Display form for editing a subject"""
    st.markdown("---")
    st.subheader(f"✏️ Edit Subject: {subject_name}")
    
    # Find the subject to edit
    subject_to_edit = None
    for subject in st.session_state.planner.subjects:
        if subject['name'] == subject_name:
            subject_to_edit = subject
            break
    
    if subject_to_edit:
        with st.form("edit_subject_form"):
            # Pre-fill form with existing values
            new_name = st.text_input("Subject Name:", value=subject_to_edit['name'])
            new_difficulty = st.selectbox(
                "Difficulty Level:", 
                ['Easy', 'Medium', 'Hard'],
                index=['Easy', 'Medium', 'Hard'].index(subject_to_edit['difficulty'])
            )
            new_priority = st.slider(
                "Priority (1-10):", 
                1, 10, subject_to_edit['priority']
            )
            new_hours = st.slider(
                "Hours per week:", 
                1, 20, subject_to_edit['hours_per_week']
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                    try:
                        success = st.session_state.planner.edit_subject(
                            subject_name, new_name, new_difficulty, new_priority, new_hours
                        )
                        if success:
                            st.success("✅ Subject updated successfully!")
                            del st.session_state.editing_subject
                            st.rerun()
                    except ValueError as e:
                        st.error(f"❌ {str(e)}")
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    del st.session_state.editing_subject
                    st.rerun()

def delete_subject_confirmation(subject_name):
    """Display confirmation dialog for deleting a subject"""
    st.markdown("---")
    st.warning(f"🗑️ Are you sure you want to delete '{subject_name}'?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Yes, Delete", use_container_width=True):
            st.session_state.planner.delete_subject(subject_name)
            st.success(f"✅ '{subject_name}' has been deleted")
            del st.session_state.deleting_subject
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            del st.session_state.deleting_subject
            st.rerun()

def main():
    # Header
    st.markdown('<h1 class="main-header">📚 AI Study Planner</h1>', unsafe_allow_html=True)
    st.markdown("### Enter subjects + study days → Get your personalized study schedule")
    
    # Initialize planner
    if 'planner' not in st.session_state:
        st.session_state.planner = AIStudyPlanner()
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("⚙️ Study Configuration")
        
        # Study days selection
        st.subheader("📅 Study Days")
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        study_days = st.multiselect(
            "Select your study days:",
            days_of_week,
            default=['Monday', 'Wednesday', 'Friday', 'Saturday'],
            help="Choose the days you want to study"
        )
        
        # Daily study hours
        daily_hours = st.slider(
            "Maximum study hours per day:",
            min_value=2,
            max_value=10,
            value=6,
            step=1,
            help="Maximum number of study hours per day"
        )
        
        # Add subject form
        add_subject_form()
        
        # Manage subjects section
        manage_subjects_section()
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="sub-header">📖 Your Subjects</div>', unsafe_allow_html=True)
        
        if not st.session_state.planner.subjects:
            st.info("👆 Add subjects using the sidebar to get started!")
        else:
            total_weekly_hours = sum(subject['hours_per_week'] for subject in st.session_state.planner.subjects)
            st.metric("Total Weekly Study Hours", f"{total_weekly_hours}h")
            
            for subject in st.session_state.planner.subjects:
                difficulty_class = f"difficulty-{subject['difficulty'].lower()}"
                st.markdown(
                    f"""
                    <div class="subject-card {difficulty_class}">
                        <h4>{subject['name']}</h4>
                        <p><strong>Difficulty:</strong> {subject['difficulty']}</p>
                        <p><strong>Priority:</strong> {subject['priority']}/10</p>
                        <p><strong>Hours/Week:</strong> {subject['hours_per_week']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Show study tips on expander
                with st.expander(f"💡 Study Tips for {subject['name']}"):
                    tips = st.session_state.planner.get_study_tips(
                        subject['name'], subject['difficulty']
                    )
                    for tip in tips:
                        st.write(f"• {tip}")
    
    with col2:
        st.markdown('<div class="sub-header">🗓️ Generated Study Schedule</div>', unsafe_allow_html=True)
        
        if study_days and st.session_state.planner.subjects:
            # Generate schedule
            st.session_state.planner.generate_schedule(study_days, daily_hours)
            
            # Display schedule
            for day, plan in st.session_state.planner.schedule.items():
                with st.container():
                    st.markdown(f"### 📅 {day}")
                    
                    if plan['subjects']:
                        total_hours = plan['total_hours']
                        progress = total_hours / daily_hours
                        
                        st.progress(progress)
                        st.write(f"**Total study hours: {total_hours}h**")
                        
                        for session in plan['subjects']:
                            difficulty_class = f"difficulty-{session['difficulty'].lower()}"
                            st.markdown(
                                f"""
                                <div class="day-schedule {difficulty_class}">
                                    <strong>{session['subject']}</strong> - {session['hours']}h 
                                    <em>({session['difficulty']})</em>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    else:
                        st.info("No study sessions scheduled")
                    
                    st.markdown("---")
            
            # Show reminders
            st.markdown('<div class="sub-header">🔔 Smart Reminders</div>', unsafe_allow_html=True)
            reminders = st.session_state.planner.generate_reminders()
            for reminder in reminders:
                st.markdown(
                    f'<div class="reminder">{reminder}</div>',
                    unsafe_allow_html=True
                )
            
            # Export options
            st.markdown("---")
            st.subheader("💾 Export Schedule")
            
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                if st.button("📊 Generate Summary", use_container_width=True):
                    # Create summary dataframe
                    summary_data = []
                    for day, plan in st.session_state.planner.schedule.items():
                        for session in plan['subjects']:
                            summary_data.append({
                                'Day': day,
                                'Subject': session['subject'],
                                'Hours': session['hours'],
                                'Difficulty': session['difficulty']
                            })
                    
                    if summary_data:
                        df = pd.DataFrame(summary_data)
                        st.dataframe(df, use_container_width=True)
            
            with col_export2:
                # Simple export as JSON
                schedule_data = {
                    'generated_at': datetime.now().isoformat(),
                    'total_subjects': len(st.session_state.planner.subjects),
                    'total_weekly_hours': total_weekly_hours,
                    'study_days': study_days,
                    'daily_hours_limit': daily_hours,
                    'subjects': st.session_state.planner.subjects,
                    'schedule': st.session_state.planner.schedule
                }
                
                st.download_button(
                    label="📥 Download Schedule",
                    data=json.dumps(schedule_data, indent=2),
                    file_name=f"study_schedule_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            if not study_days:
                st.warning("📅 Please select study days in the sidebar")
            if not st.session_state.planner.subjects:
                st.warning("📚 Please add subjects using the form in the sidebar")

if __name__ == "__main__":
    main()