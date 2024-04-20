import matplotlib.pyplot as plt
import streamlit as st
from anastruct import SystemElements

# Create a SystemElements object
ss = SystemElements()
st.sidebar.title('Structural Analysis - Calculator')
st.sidebar.subheader('Select No of Elements')
elements = st.sidebar.number_input("Number of Elements", min_value=1, step=1, value=1)

try:
    previous_x2 = 0.0  # Initialize the x-coordinate of the end point of the previous element
    previous_y2 = 0.0  # Initialize the y-coordinate of the end point of the previous element

    for i in range(elements):
        st.sidebar.markdown(f"## Element {i + 1}")
        x1 = previous_x2  # Set the x-coordinate of the start point of the current element to the end point of the previous element
        y1 = previous_y2  # Set the y-coordinate of the start point of the current element to the end point of the previous element
        x2 = st.sidebar.text_input(f"X-coordinate of node 2 of Element {i + 1}", value=1.0)
        y2 = st.sidebar.text_input(f"Y-coordinate of node 2 of Element {i + 1}", value=0.0)
        ss.add_element(location=[[float(x1), float(y1)], [float(x2), float(y2)]])

        previous_x2 = float(x2)  # Update the x-coordinate of the end point of the previous element for the next iteration
        previous_y2 = float(y2)  # Update the y-coordinate of the end point of the previous element for the next iteration

except Exception as e:
    st.error(f"Continue to add coordinates to Element {2} to avoid {e}")

# Sidebar title for supports
st.sidebar.subheader('Add Supports')

# Ask the user for the number of supports
no_of_supports = st.sidebar.number_input("Number of Supports", min_value=1, step=1, value=1)

# Loop through each support
for i in range(no_of_supports):
    st.sidebar.markdown(f"## Support {i + 1}")
    support_node = st.sidebar.number_input(f"Select node for Support {i + 1}", min_value=1, step=1, value=1)
    support_type = st.sidebar.radio(f"Select support type for Support {i + 1}", ("Fixed", "Hinged", "Roller"))

    # Apply the selected support to the selected node
    if support_type == "Fixed":
        ss.add_support_fixed(node_id=support_node)
    elif support_type == "Hinged":
        ss.add_support_hinged(node_id=support_node)
    elif support_type == "Roller":
        ss.add_support_roll(node_id=support_node)

# Ask the user for the number of loads
no_of_loads = st.sidebar.number_input("Number of Loads", min_value=1, step=1, value=1)

# Loop through each load
for i in range(no_of_loads):
    st.sidebar.markdown(f"## Load {i + 1}")
    load_type = st.sidebar.radio(f"Select the type of Load", ('Point', 'UDL'), key=f"load_type_{i}")
    if load_type == "Point":
        load_node = st.sidebar.number_input(f'Select the node for load {i + 1}', min_value=1, step=1, value=1)
        p_load_direction = st.sidebar.radio(f"Load Direction", ('Fx', 'Fy'), key=f"load_direction_{i}")
        if p_load_direction == 'Fx':
            p_load = st.sidebar.text_input(f"Enter Load Magnitude at {i + 1}", value=1)
            ss.point_load(node_id=int(load_node), Fx=int(p_load))
        elif p_load_direction == 'Fy':
            p_load = st.sidebar.text_input(f"Enter Load Magnitude at {i + 1}", value=1)
            ss.point_load(node_id=int(load_node), Fy=int(p_load))

    elif load_type == "UDL":
        load_element = st.sidebar.number_input(f'Select the Element for load {i + 1}', min_value=1, step=1, value=1)
        q_load = st.sidebar.text_input(f"Enter Load Magnitude at {i + 1}", value=1)
        ss.q_load(q=int(q_load), element_id=int(load_element))

# Solve the system
ss.solve()

# Show Structure
fig_structure = ss.show_structure(show=False, )
st.subheader("Structure")
plt.savefig('structure.png')
st.image('structure.png')


button_width = 150

m = st.markdown("""
<style>
div.stButton > button:first-child {
    width: 150px;
    
}   
</style>""", unsafe_allow_html=True)

# Show buttons in the same row
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)


if col1.button('Reactions', type='primary',):
    # Show Reactions
    fig_reactions = ss.show_reaction_force(show=False, )
    st.subheader("Reaction Force")
    plt.savefig('reactions.png')
    st.image('reactions.png')

if col2.button('Shear Force', type='primary'):
    # Show Shear Force
    fig_shearforce = ss.show_shear_force(show=False, )
    st.subheader("Shear Force")
    plt.savefig('sf.png')
    st.image('sf.png')

if col3.button('BMD', type='primary'):
    # Show Bending Moment
    fig_bmd = ss.show_bending_moment(show=False, )
    st.subheader("Bending Moment")
    plt.savefig('bmd.png')
    st.image('bmd.png')

if col4.button('Displacement', type='primary'):
    # Show Displacement
    fig_displacement = ss.show_displacement(show=False, )
    st.subheader("Displacement")
    plt.savefig('disp.png')
    st.image('disp.png')

if col5.button('Axial Force', type='primary'):
    # Show Axial Force
    fig_axial_force = ss.show_axial_force(show=False, )
    st.subheader("Axial Force")
    plt.savefig('af.png')
    st.image('af.png')

if col6.button('Beam Results', type='primary'):
    # Show All Beam Results
    fig_axial_force = ss.show_results(show=False, figsize=(12, 12))
    st.subheader("Beam Result")
    plt.savefig('beam_result.png')
    st.image('beam_result.png')