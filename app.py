import streamlit as st
import copy
from cube import Cube, stringToCube, cubeToString
import huffy_code

# Configure page
st.set_page_config(
    page_title="Virtual Rubik's Cube - String Encoder",
    page_icon="🧩",
    layout="wide"
)

def get_color_style(color_char):
    """Convert cube color character to CSS background color"""
    color_map = {
        'r': '#FF0000',  # Red
        'g': '#00FF00',  # Green  
        'b': '#0000FF',  # Blue
        'y': '#FFFF00',  # Yellow
        'w': '#FFFFFF',  # White
        'o': '#FFA500',  # Orange
        ' ': '#CCCCCC'   # Gray for empty spaces
    }
    return color_map.get(color_char.lower(), '#CCCCCC')

def display_cube(cube):
    """Display the cube with colors using Streamlit columns"""
    lines = cube.lines.split('\n')
    
    st.markdown("### Current Cube State")
    
    # Use a simple text-based approach with colored backgrounds
    for line in lines:
        cols = st.columns(len(line) if line else 1)
        for i, char in enumerate(line):
            if i < len(cols):
                color = get_color_style(char)
                if char != ' ':
                    cols[i].markdown(
                        f"""<div style='
                            background-color: {color};
                            color: {'black' if char in ['y', 'w'] else 'white'};
                            text-align: center;
                            padding: 8px;
                            border: 1px solid #000;
                            font-family: monospace;
                            font-weight: bold;
                        '>{char}</div>""",
                        unsafe_allow_html=True
                    )
                else:
                    cols[i].markdown("<div style='padding: 8px;'>&nbsp;</div>", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'cube' not in st.session_state:
        st.session_state.cube = Cube(3)
    if 'last_solution' not in st.session_state:
        st.session_state.last_solution = ""
    if 'last_reverse_solution' not in st.session_state:
        st.session_state.last_reverse_solution = ""
    if 'last_extracted_string' not in st.session_state:
        st.session_state.last_extracted_string = ""

def main():
    st.title("🧩 Virtual Rubik's Cube - String Encoder")
    st.markdown("*Encode short strings into Rubik's cube configurations using Huffman compression*")
    
    initialize_session_state()
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display the cube
        display_cube(st.session_state.cube)
        
        # Cube status
        if st.session_state.cube.is_solved():
            st.success("✅ Cube is solved!")
        else:
            st.info("🔄 Cube is scrambled")
    
    with col2:
        st.markdown("### Controls")
        
        # Set String section
        st.markdown("#### 📝 Set String")
        input_string = st.text_input("Enter string to encode:", key="string_input")
        
        if st.button("Set String", type="primary"):
            if input_string.strip():
                try:
                    # Check string length and show warning if needed
                    as_number = huffy_code.to_number(input_string)
                    max_number = 43252003274489856000
                    
                    if as_number >= max_number:
                        st.warning(f"⚠️ Warning: String is too long! (Number: {as_number:,})")
                        st.write("Proceeding anyway to show result...")
                    
                    # Convert string to cube
                    st.session_state.cube = stringToCube(input_string)
                    
                    # Get reverse solution (to reach this scrambled state)
                    st.session_state.last_reverse_solution = st.session_state.cube.get_reverse_solution()
                    
                    st.success(f"✅ String '{input_string}' encoded into cube!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error encoding string: {str(e)}")
            else:
                st.error("Please enter a string to encode")
        
        # Get String section
        st.markdown("#### 📤 Get String")
        if st.button("Extract String from Cube"):
            try:
                extracted = cubeToString(st.session_state.cube)
                st.session_state.last_extracted_string = extracted
                if extracted.strip():
                    st.success(f"📝 Extracted: **{extracted}**")
                else:
                    st.info("No string found (cube may be in solved state)")
            except Exception as e:
                st.error(f"Error extracting string: {str(e)}")
        
        if st.session_state.last_extracted_string:
            st.code(st.session_state.last_extracted_string)
        
        # Solve section
        st.markdown("#### 🎯 Solve Cube")
        if st.button("Get Solution"):
            try:
                solution = st.session_state.cube.get_solution()
                st.session_state.last_solution = solution
                st.success("Solution found!")
            except Exception as e:
                st.error(f"Error getting solution: {str(e)}")
        
        if st.session_state.last_solution:
            st.markdown("**Solution steps:**")
            st.code(st.session_state.last_solution)
        
        # Reverse Solve section
        st.markdown("#### 🔄 Reverse Solution")
        st.caption("Shows how to reach the current scrambled state from solved")
        if st.session_state.last_reverse_solution:
            st.markdown("**Steps to reach this state:**")
            st.code(st.session_state.last_reverse_solution)
        
        # Utility buttons
        st.markdown("#### 🎲 Cube Actions")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎲 Scramble"):
                st.session_state.cube.scramble()
                st.session_state.last_solution = ""
                st.session_state.last_reverse_solution = ""
                st.rerun()
        
        with col_b:
            if st.button("🔄 Reset"):
                st.session_state.cube = Cube(3)
                st.session_state.last_solution = ""
                st.session_state.last_reverse_solution = ""
                st.session_state.last_extracted_string = ""
                st.rerun()
    
    # Information section
    st.markdown("---")
    st.markdown("### ℹ️ How it works")
    with st.expander("Click to learn more"):
        st.markdown("""
        **String Encoding:**
        - Uses Huffman compression to convert text into numbers
        - Numbers are mapped to valid Rubik's cube configurations
        - Maximum recommended string length: ~12-15 characters
        
        **Features:**
        - **Set String**: Encode text into cube configuration
        - **Get String**: Extract encoded text from current cube
        - **Solve**: Get steps to solve the current cube
        - **Reverse Solve**: Get steps to reach current state from solved
        - **Scramble/Reset**: Manipulate cube state
        
        **Note:** The reverse solution is especially useful when you've encoded a string - 
        it shows you how to manually create that encoded state from a solved cube!
        """)

if __name__ == "__main__":
    main()