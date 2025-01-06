import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import zipfile
import io

# Event details
events = {
    "Wedding Reception": {
        "date": "2nd February 2025",
        "time": "13:00",
        "venue": "Beechwood Gardens (25 Christopherson Street, Hyde Park, Sandton)",
        "dress_code": "Smart-Casual",
        "link": "https://www.google.com/maps/place/Beechwood+Gardens/@-26.1322665,28.0384948,17z/data=!3m1!4b1!4m6!3m5!1s0x1e950cbf90f02587:0xa5acf013bfd8780d!8m2!3d-26.1322713!4d28.0410697!16s%2Fg%2F11b6d4zg8l?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
    },
    "Nikkah": {
        "date": "1st February 2025",
        "time": "9:45 AM (Note: Please try be on time due to limited time at the venue)",
        "venue": "Nizamiye Mosque (Le Roux Avenue, Allandale, Midrand)",
        "dress_code": "Casual",
        "link": "https://www.google.com/maps/place/Nizamiye+Mosque/@-26.0145413,28.1269714,17z/data=!3m1!4b1!4m6!3m5!1s0x1e956de42eda71b3:0xe45cbc311e28a07c!8m2!3d-26.0145461!4d28.1295463!16s%2Fm%2F0n53q9j?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
    },
    "Mendi Night (Women)": {
        "date": "1st February 2025",
        "time": "18:00",
        "venue": "Argentinean Association Mark's Park (Judith Avenue, Emmerentia)",
        "dress_code": "Bollywood",
        "link": "https://www.google.com/maps/place/Argentinean+Association+of+South+Africa/@-26.1650127,28.0006367,17z/data=!3m1!4b1!4m6!3m5!1s0x1e950b9cfdbe4a6b:0x303fb2423e70c3d2!8m2!3d-26.1650175!4d28.0032116!16s%2Fg%2F11h0xs7j_?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
    },
    "Mendi Night (Men)": {
        "date": "1st February 2025",
        "time": "20:30",
        "venue": "Argentinean Association Mark's Park (Judith Avenue, Emmerentia)",
        "dress_code": "Bollywood",
        "link": "https://www.google.com/maps/place/Argentinean+Association+of+South+Africa/@-26.1650127,28.0006367,17z/data=!3m1!4b1!4m6!3m5!1s0x1e950b9cfdbe4a6b:0x303fb2423e70c3d2!8m2!3d-26.1650175!4d28.0032116!16s%2Fg%2F11h0xs7j_?authuser=0&entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
    },
    "Pre-Wedding Dinner (Adam)": {
        "date": "31st January 2025",
        "time": "18:00",
        "venue": "To Be Confirmed (TBC)",
        "dress_code": "Casual",
        "link": "Link to Venue (TBC)"
    },
    "Pre-Wedding Party": {
        "date": "30th January 2025",
        "time": "19:00",
        "venue": "To Be Confirmed (TBC)",
        "dress_code": "Casual",
        "link": "Link to Venue (TBC)"
    }
}

# Invitation groups
invitation_groups = {
    "1/2": ["Wedding Reception", "Nikkah"],
    "1/2/3": ["Wedding Reception", "Nikkah", "Mendi Night (Women)"],
    "1/2/3/5": ["Wedding Reception", "Nikkah", "Mendi Night (Women)", "Pre-Wedding Dinner (Adam)"],
    "1/2/3/4/5": ["Wedding Reception", "Nikkah", "Mendi Night (Women)", "Mendi Night (Men)", "Pre-Wedding Dinner (Adam)"],
    "1/2/3/5/6": ["Wedding Reception", "Nikkah", "Mendi Night (Women)", "Pre-Wedding Dinner (Adam)", "Pre-Wedding Party"],
    "1/2/4": ["Wedding Reception", "Nikkah", "Mendi Night (Men)"],
    "1/2/4/5": ["Wedding Reception", "Nikkah", "Mendi Night (Men)", "Pre-Wedding Dinner (Adam)"],
    "1/2/4/5/6": ["Wedding Reception", "Nikkah", "Mendi Night (Men)", "Pre-Wedding Dinner (Adam)", "Pre-Wedding Party"],
    "1/2/5": ["Wedding Reception", "Nikkah", "Pre-Wedding Dinner (Adam)"],
    "2": ["Nikkah"],
    "2/5": ["Nikkah", "Pre-Wedding Dinner (Adam)"]
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
    "3": "Mendi Night (Women)",
    "4": "Mendi Night (Men)",
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

# Button to generate invitations
if st.button("Generate Invitations"):
    st.write("Generating invitations...")
    invite_files = []
    
    for _, row in edited_guest_list.iterrows():
        guest_name = row["Guest Name"]
        group_type = row["Group Type"]
        events_for_group = invitation_groups[group_type]
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Title with guest name
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt=f"Itinerary - {guest_name}", ln=True, align="C")
        pdf.ln(10)
        
        # Event Details
        for event_name in events_for_group:
            event = events[event_name]
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(200, 10, txt=event_name, ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Date: {event['date']}", ln=True)
            pdf.cell(200, 10, txt=f"Time: {event['time']}", ln=True)
            pdf.cell(200, 10, txt=f"Dress Code: {event['dress_code']}", ln=True)

            # Add clickable venue name as the link
            pdf.set_text_color(0, 0, 255)  # Blue color for hyperlink
            pdf.set_font("Arial", style="U", size=12)  # Underline for clickable text
            pdf.cell(200, 10, txt=event["venue"], ln=True, link=event["link"])
            pdf.set_text_color(0, 0, 0)  # Reset color to black
            pdf.set_font("Arial", size=12)  # Reset font style
            pdf.ln(10)
        
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
