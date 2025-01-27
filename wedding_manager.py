import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import zipfile
import io
from datetime import datetime

# Event details
events = {
    "Wedding Reception": {
        "date": "2025-02-02",
        "time": "13:00",
        "venue": "Beechwood Gardens (25 Christopherson Street, Hyde Park, Sandton)",
        "dress_code": "Black-Tie/Formal",
        "link": "https://www.google.com/maps/place/Beechwood+Gardens/@-26.1322665,28.0384948,17z/data=!3m1!4b1!4m6!3m5!1s0x1e950cbf90f02587:0xa5acf013bfd8780d!8m2!3d-26.1322713!4d28.0410697!16s%2Fg%2F11b6d4zg8l?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
    },
    "Nikkah": {
        "date": "2025-02-01",
        "time": "9:45 AM (Note: Please try be on time due to limited time at the venue)",
        "venue": "Nizamiye Mosque (Le Roux Avenue, Allandale, Midrand)",
        "dress_code": "Modest/Islamic-Attire",
        "link": "https://www.google.com/maps/place/Nizamiye+Mosque/@-26.0145413,28.1269714,17z/data=!3m1!4b1!4m6!3m5!1s0x1e956de42eda71b3:0xe45cbc311e28a07c!8m2!3d-26.0145461!4d28.1295463!16s%2Fm%2F0n53q9j?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
    },
    "Mendi Night (Invited Women)": {
        "date": "2025-02-01",
        "time": "18:00",
        "venue": "Argentinean Association, Mark's Park (Judith Avenue, Emmerentia)",
        "dress_code": "Bollywood",
        "link": "https://www.google.com/maps/place/Argentinean+Association+of+South+Africa/@-26.1650127,28.0006367,17z/data=!3m1!4b1!4m6!3m5!1s0x1e950b9cfdbe4a6b:0x303fb2423e70c3d2!8m2!3d-26.1650175!4d28.0032116!16s%2Fg%2F11h0xs7j_?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
    },
    "Mendi Night (After Party)": {
        "date": "2025-02-01",
        "time": "20:30",
        "venue": "Argentinean Association, Mark's Park (Judith Avenue, Emmerentia)",
        "dress_code": "Bollywood",
        "link": "https://www.google.com/maps/place/Argentinean+Association+of+South+Africa/@-26.1650127,28.0006367,17z/data=!3m1!4b1!4m6!3m5!1s0x1e950b9cfdbe4a6b:0x303fb2423e70c3d2!8m2!3d-26.1650175!4d28.0032116!16s%2Fg%2F11h0xs7j_?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
    },
    "Pre-Wedding Dinner (Adam)": {
        "date": "2025-01-31",
        "time": "18:30",
        "venue": "The Houghton Terrace (No. 3 15th Avenue, Houghton)",
        "dress_code": "Smart-Casual",
        "link": "https://www.google.com/maps/place/Houghton+Terrace/@-26.1501413,28.0570936,17z/data=!3m1!4b1!4m6!3m5!1s0x1e950cff33410b1d:0x6e1c2a40df568d0!8m2!3d-26.1501461!4d28.0596685!16s%2Fg%2F11h4yr6tk3?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
    },
    "Ultra-Themed Party": {
        "date": "2025-01-30",
        "time": "18:30",
        "venue": "To Be Confirmed (TBC)",
        "dress_code": "Casual",
        "link": "Link to Venue (TBC)"
    }
}

# Invitation groups
invitation_groups = {
    "1/2": ["Wedding Reception", "Nikkah"],
    "1/2/3": ["Wedding Reception", "Nikkah", "Mendi Night (Invited Women)"],
    "1/2/3/5": ["Wedding Reception", "Nikkah", "Mendi Night (Invited Women)", "Pre-Wedding Dinner (Adam)"],
    "1/2/3/4/5": ["Wedding Reception", "Nikkah", "Mendi Night (After Party)", "Mendi Night (Invited Women)", "Pre-Wedding Dinner (Adam)"],
    "1/2/3/5/6": ["Wedding Reception", "Nikkah", "Mendi Night (Invited Women)", "Pre-Wedding Dinner (Adam)", "Ultra-Themed Party"],
    "1/2/4": ["Wedding Reception", "Nikkah", "Mendi Night (After Party)"],
    "1/2/4/5": ["Wedding Reception", "Nikkah", "Mendi Night (After Party)", "Pre-Wedding Dinner (Adam)"],
    "1/2/4/5/6": ["Wedding Reception", "Nikkah", "Mendi Night (After Party)", "Pre-Wedding Dinner (Adam)", "Ultra-Themed Party"],
    "1/2/5": ["Wedding Reception", "Nikkah", "Pre-Wedding Dinner (Adam)"],
    "2": ["Nikkah"],
    "2/5": ["Nikkah", "Pre-Wedding Dinner (Adam)"],
    "1/2/3/6": ["Wedding Reception", "Nikkah", "Mendi Night (Invited Women)", "Ultra-Themed Party"],
    "1/2/4/6": ["Wedding Reception", "Nikkah", "Mendi Night (After Party)", "Ultra-Themed Party"],
    "1/2/3/4/6": ["Wedding Reception", "Nikkah", "Mendi Night (After Party)", "Mendi Night (Invited Women)", "Ultra-Themed Party"],
}

# Load or create guest list
def load_guest_list():
    """Load guest list from a CSV file or create a default list."""
    file_path = "guest_list.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # Default guest list
        return pd.DataFrame({
            "Guest Name": ["Adam's Mom", "Shahana's Aunty", "Best Friend", "Family Friend", "Work Colleague"],
            "Group Type": ["1/2", "1/2/3", "1/2/3/5", "2", "1/2/4/5"]
        })

def save_guest_list(guest_list):
    """Save guest list to a CSV file."""
    guest_list.to_csv("guest_list.csv", index=False)

# Load the guest list
guest_list = load_guest_list()

# Main interface
st.title("Adam x Shahana Wedding Invitation Manager")

# Event mapping
event_definitions = {
    "1": "Wedding Reception",
    "2": "Nikkah",
    "3": "Mendi Night (Invited Women)",
    "4": "Mendi Night (After Party)",
    "5": "Pre-Wedding Dinner (Adam)",
    "6": "Pre-Wedding Party"
}

# Display Event Definitions
st.write("### Event Definitions")
for number, event_name in event_definitions.items():
    st.write(f"**{number}:** {event_name}")

st.write("### Guest List")
st.write("Manage guest names and group types dynamically:")

# Editable data table
edited_guest_list = st.data_editor(guest_list, num_rows="dynamic")

# Save changes if the guest list is modified
if st.button("Save Guest List"):
    save_guest_list(edited_guest_list)
    st.success("Guest list saved successfully!")

if st.button("Generate Invitations"):
    st.write("Generating invitations...")
    invite_files = []
    
    for _, row in edited_guest_list.iterrows():
        guest_name = row["Guest Name"]
        group_type = row["Group Type"]
        events_for_group = invitation_groups[group_type]
        
        # Reverse the order of the events
        sorted_events = events_for_group[::-1]
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)  # Smaller font size for the entire PDF
        
        # Title with guest name
        pdf.set_font("Arial", style="B", size=12)  # Slightly larger title font
        pdf.cell(200, 8, txt=f"Itinerary - {guest_name}", ln=True, align="C")
        pdf.ln(5)  # Reduce space below the title
        
        # Event Details
        for event_name in sorted_events:
            event = events[event_name]
            pdf.set_font("Arial", style="B", size=10)  # Smaller bold font for event name
            pdf.cell(200, 6, txt=event_name, ln=True)  # Reduced line height

            # Format the date to "Day-of-Week, Day Month Year"
            formatted_date = datetime.strptime(event["date"], "%Y-%m-%d").strftime("%A, %d %B %Y")
            pdf.set_font("Arial", size=9)  # Smaller font for details
            pdf.cell(200, 6, txt=f"Date: {formatted_date}", ln=True)
            
            pdf.cell(200, 6, txt=f"Time: {event['time']}", ln=True)
            pdf.cell(200, 6, txt=f"Dress Code: {event['dress_code']}", ln=True)

            # Add clickable venue name as the link
            pdf.set_text_color(0, 0, 255)  # Blue color for hyperlink
            pdf.set_font("Arial", style="U", size=9)  # Smaller underlined font for links
            pdf.cell(200, 6, txt=event["venue"], ln=True, link=event["link"])
            pdf.set_text_color(0, 0, 0)  # Reset color to black
            pdf.set_font("Arial", size=9)  # Reset font style
            pdf.ln(3)  # Smaller line spacing between events
        
        # Save PDF
        file_path = f"Invitation_{guest_name.replace(' ', '_')}_{group_type.replace('/', '_')}.pdf"
        pdf.output(file_path)
        invite_files.append(file_path)
    
    st.success("Invitations generated!")
    
    # Display download links for individual files
    for file in invite_files:
        with open(file, "rb") as f:
            st.download_button(
                label=f"Download {os.path.basename(file)}",
                data=f,
                file_name=file,
                mime="application/pdf"
            )
    
    # Create a ZIP file containing all the invitations
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for file in invite_files:
            zip_file.write(file)
    zip_buffer.seek(0)

    # Add "Download All" button
    st.download_button(
        label="Download All Invitations as ZIP",
        data=zip_buffer,
        file_name="All_Invitations.zip",
        mime="application/zip"
    )
