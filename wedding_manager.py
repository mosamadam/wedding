import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Event details
events = {
    "Wedding Reception": {
        "date": "2nd February 2025",
        "time": "13:00",
        "venue": "Beechwood Gardens (25 Christopherson Street, Hyde Park, Sandton)",
        "dress_code": "Smart-Casual",
        "link": "Link to Beechwood Gardens"
    },
    "Nikkah": {
        "date": "1st February 2025",
        "time": "9:45 AM",
        "venue": "Nizamiye Mosque (Le Roux Avenue, Allandale, Midrand)",
        "dress_code": "Casual",
        "link": "Link to Nizamiye Mosque"
    },
    "Mendi Night (Women)": {
        "date": "1st February 2025",
        "time": "18:00",
        "venue": "Argentinean Association Mark's Park (Judith Avenue, Emmerentia)",
        "dress_code": "Bollywood",
        "link": "Link to Mark's Park"
    },
    "Mendi Night (Men)": {
        "date": "1st February 2025",
        "time": "20:30",
        "venue": "Argentinean Association Mark's Park (Judith Avenue, Emmerentia)",
        "dress_code": "Bollywood",
        "link": "Link to Mark's Park"
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
    "1/2/3/5/6": ["Wedding Reception", "Nikkah", "Mendi Night (Women)", "Pre-Wedding Dinner (Adam)", "Pre-Wedding Party"],
    "1/2/4": ["Wedding Reception", "Nikkah", "Mendi Night (Men)"],
    "1/2/4/5": ["Wedding Reception", "Nikkah", "Mendi Night (Men)", "Pre-Wedding Dinner (Adam)"],
    "1/2/4/5/6": ["Wedding Reception", "Nikkah", "Mendi Night (Men)", "Pre-Wedding Dinner (Adam)", "Pre-Wedding Party"],
    "2": ["Nikkah"],
    "2/5": ["Nikkah", "Pre-Wedding Dinner (Adam)"]
}

# Load or create guest list
@st.cache_data
def load_guest_list():
    return pd.DataFrame({
        "Guest Name": ["Adam's Dad", "Shahana's Mom", "Best Friend", "Family Friend", "Work Colleague"],
        "Group Type": ["1/2", "1/2/3", "1/2/3/5", "2", "1/2/4/5"]
    })

guest_list = load_guest_list()

# Main interface
st.title(" Adam x Shahana Wedding Invitation Manager")


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

# Button to generate invites
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
            pdf.cell(200, 10, txt=f"Venue: {event['venue']}", ln=True)
            pdf.cell(200, 10, txt=f"Dress Code: {event['dress_code']}", ln=True)
            pdf.cell(200, 10, txt=f"Venue Link: {event['link']}", ln=True)
            pdf.ln(10)
        
        # Save PDF
        file_path = f"Invitation_{guest_name.replace(' ', '_')}_{group_type.replace('/', '_')}.pdf"
        pdf.output(file_path)
        invite_files.append(file_path)
    
    st.success("Invitations generated!")
    
    # Display download links for generated PDFs
    for file in invite_files:
        with open(file, "rb") as f:
            st.download_button(
                label=f"Download {os.path.basename(file)}",
                data=f,
                file_name=file,
                mime="application/pdf"
            )

    
    # test
