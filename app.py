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

def display_cube(cube, editable=False):
    """Display the cube with colors using Streamlit columns"""
    lines = cube.lines.split('\n')
    
    st.markdown("### Current Cube State")
    
    if editable and 'active_color' in st.session_state:
        st.info("🎨 Paint mode active! Click on squares to change their color.")
    
    # Use a simple text-based approach with colored backgrounds
    for row_idx, line in enumerate(lines):
        cols = st.columns(len(line) if line else 1)
        for col_idx, char in enumerate(line):
            if col_idx < len(cols):
                color = get_color_style(char)
                if char != ' ':
                    if editable and 'active_color' in st.session_state:
                        # Make clickable for editing
                        button_key = f"cube_{row_idx}_{col_idx}"
                        if cols[col_idx].button(
                            char,
                            key=button_key,
                            help=f"Click to paint with {st.session_state.active_color}",
                            use_container_width=True
                        ):
                            # Update the cube state
                            update_cube_square(row_idx, col_idx, st.session_state.active_color)
                            st.rerun()
                    else:
                        # Regular display
                        cols[col_idx].markdown(
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
                    cols[col_idx].markdown("<div style='padding: 8px;'>&nbsp;</div>", unsafe_allow_html=True)

def update_cube_square(row_idx, col_idx, new_color):
    """Update a specific square in the cube"""
    lines = st.session_state.cube.lines.split('\n')
    if row_idx < len(lines) and col_idx < len(lines[row_idx]):
        line_list = list(lines[row_idx])
        line_list[col_idx] = new_color
        lines[row_idx] = ''.join(line_list)
        st.session_state.cube.lines = '\n'.join(lines)

def create_color_palette():
    """Create a color palette for painting the cube"""
    paint_mode = st.session_state.get('paint_mode', False)
    
    if paint_mode:
        st.markdown("#### 🎨 Cube Editor")
        
        # Color options
        colors = {
            'Red': 'r',
            'Green': 'g',
            'Blue': 'b',
            'Yellow': 'y',
            'White': 'w',
            'Orange': 'o'
        }
        
        # Create color selection buttons
        cols = st.columns(6)
        for i, (color_name, color_char) in enumerate(colors.items()):
            color_style = get_color_style(color_char)
            with cols[i]:
                if st.button(
                    color_name,
                    key=f"color_{color_char}",
                    help=f"Select {color_name} as active color",
                    use_container_width=True
                ):
                    st.session_state.active_color = color_char
                    st.rerun()
        
        # Show active color
        if 'active_color' in st.session_state:
            active_color_style = get_color_style(st.session_state.active_color)
            active_name = [name for name, char in colors.items() if char == st.session_state.active_color][0]
            st.markdown(
                f"""<div style='
                    background-color: {active_color_style};
                    color: {'black' if st.session_state.active_color in ['y', 'w'] else 'white'};
                    text-align: center;
                    padding: 10px;
                    border: 2px solid #000;
                    font-weight: bold;
                    margin: 10px 0;
                '>Active Color: {active_name}</div>""",
                unsafe_allow_html=True
            )
        
        # Exit paint mode
        if st.button("👁️ Exit Paint Mode", use_container_width=True):
            if 'paint_mode' in st.session_state:
                del st.session_state.paint_mode
            st.rerun()
    else:
        # Show manual rotation controls when not in paint mode
        st.markdown("#### 🔄 Manual Rotations")
        
        # Face rotations
        st.markdown("**Face Rotations:**")
        face_cols = st.columns(6)
        faces = ['U', 'D', 'L', 'R', 'F', 'B']
        for i, face in enumerate(faces):
            with face_cols[i]:
                if st.button(f"{face}", key=f"rot_{face}", help=f"Rotate {face} face clockwise"):
                    st.session_state.cube.do_command(face)
                    st.rerun()
        
        # Prime rotations
        st.markdown("**Counter-clockwise:**")
        prime_cols = st.columns(6)
        for i, face in enumerate(faces):
            with prime_cols[i]:
                if st.button(f"{face}'", key=f"rot_{face}_prime", help=f"Rotate {face} face counter-clockwise"):
                    st.session_state.cube.do_command(f"{face}'")
                    st.rerun()
        
        # Double rotations
        st.markdown("**Double rotations:**")
        double_cols = st.columns(6)
        for i, face in enumerate(faces):
            with double_cols[i]:
                if st.button(f"{face}2", key=f"rot_{face}_2", help=f"Rotate {face} face 180°"):
                    st.session_state.cube.do_command(f"{face}2")
                    st.rerun()
        
        # Enter paint mode
        if st.button("🎨 Enter Paint Mode", use_container_width=True):
            if 'active_color' not in st.session_state:
                st.session_state.active_color = 'r'  # Default to red
            st.session_state.paint_mode = True
            st.rerun()

def initialize_session_state():
    """Initialize session state variables"""
    if 'cube' not in st.session_state:
        st.session_state.cube = Cube(3)
    if 'last_reverse_solution' not in st.session_state:
        st.session_state.last_reverse_solution = ""
    if 'warning_message' not in st.session_state:
        st.session_state.warning_message = ""

def main():
    st.title("🧩 Virtual Rubik's Cube - String Encoder")
    st.markdown("*Encode short strings into Rubik's cube configurations using Huffman compression*")
    
    initialize_session_state()
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display the cube (editable if in paint mode)
        paint_mode = st.session_state.get('paint_mode', False)
        display_cube(st.session_state.cube, editable=paint_mode)
        
        # Cube status
        if st.session_state.cube.is_solved():
            st.success("✅ Cube is solved!")
        else:
            st.info("🔄 Cube is scrambled")
        
        # Color palette for manual editing
        create_color_palette()
    
    with col2:
        st.markdown("### Controls")
        
        # Set String section
        st.markdown("#### 📝 Set String")
        input_string = st.text_input("Enter string to encode:", key="string_input")
        
        # Show persistent warning if exists
        if st.session_state.warning_message:
            st.warning(st.session_state.warning_message)
        
        if st.button("Set String", type="primary"):
            if input_string.strip():
                try:
                    # Check string length and show warning if needed
                    as_number = huffy_code.to_number(input_string)
                    max_number = 43252003274489856000
                    
                    if as_number >= max_number:
                        st.session_state.warning_message = f"⚠️ Warning: String '{input_string}' is too long! (Number: {as_number:,}) - Proceeding anyway to show result."
                    else:
                        st.session_state.warning_message = ""  # Clear warning
                    
                    # Convert string to cube
                    st.session_state.cube = stringToCube(input_string)
                    
                    # Get reverse solution (to reach this scrambled state)
                    try:
                        st.session_state.last_reverse_solution = st.session_state.cube.get_reverse_solution()
                    except Exception as e:
                        st.session_state.last_reverse_solution = f"Error: {str(e)}"
                    
                    st.success(f"✅ String '{input_string}' encoded into cube!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error encoding string: {str(e)}")
                    st.session_state.warning_message = ""  # Clear warning on error
            else:
                st.error("Please enter a string to encode")
        
        # Always show extracted string
        st.markdown("#### 📤 Decoded String")
        try:
            extracted = cubeToString(st.session_state.cube)
            if extracted.strip():
                st.code(extracted)
            else:
                st.info("No string encoded (cube may be in solved state)")
        except Exception as e:
            st.error(f"Error extracting string: {str(e)}")
        
        # Always show current solution
        st.markdown("#### 🎯 Current Solution")
        try:
            solution = st.session_state.cube.get_solution()
            if solution.strip():
                st.markdown("**Steps to solve this cube:**")
                st.code(solution)
            else:
                st.success("✅ Cube is already solved!")
        except Exception as e:
            st.error(f"Error getting solution: {str(e)}")
        
        # Always show reverse solution if available
        if st.session_state.last_reverse_solution:
            st.markdown("#### 🔄 How to Create This State")
            st.caption("Steps to reach this state from a solved cube")
            st.markdown("**Steps from solved cube:**")
            st.code(st.session_state.last_reverse_solution)
        
        # Utility buttons
        st.markdown("#### 🎲 Cube Actions")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎲 Scramble"):
                st.session_state.cube.scramble()
                st.session_state.last_reverse_solution = ""
                st.session_state.warning_message = ""  # Clear warnings
                st.rerun()
        
        with col_b:
            if st.button("🔄 Reset"):
                st.session_state.cube = Cube(3)
                st.session_state.last_reverse_solution = ""
                st.session_state.warning_message = ""  # Clear warnings
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
        - **Cube Editor**: Manually paint cube squares with color palette
        - **Solve**: Get steps to solve the current cube
        - **Reverse Solve**: Get steps to reach current state from solved
        - **Scramble/Reset**: Manipulate cube state
        
        **Note:** The reverse solution is especially useful when you've encoded a string -
        it shows you how to manually create that encoded state from a solved cube!
        """)
    
    # Attribution section
    st.markdown("---")
    st.markdown("### 🙏 Acknowledgments")
    st.markdown("""
    **Cube Solving Library:** This application uses the [kociemba library](https://github.com/muodov/kociemba)
    for Rubik's cube solving, implemented by Daniil Kazantsev.
    """)

if __name__ == "__main__":
    main()