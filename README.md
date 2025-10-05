# 🧩 Virtual Rubik's Cube - String Encoder

A Streamlit web application that encodes short strings into Rubik's cube configurations using Huffman compression.

## Features

- **🎨 Colorful Cube Visualization**: Basic cube visualization
- **📝 String Encoding**: Convert text into unique cube configurations
- **📤 String Extraction**: Retrieve encoded text from cube states
- **🎯 Solve Functionality**: Get solution steps to solve any cube configuration
- **🔄 Reverse Solve**: Get steps to reach a specific scrambled state from solved
- **🎲 Interactive Controls**: Scramble and reset cube states

## 🌐 Try It Live

**[🚀 Try the app now at https://text-in-rubiks.streamlit.app/](https://text-in-rubiks.streamlit.app/)**

No installation required! The application is publicly hosted on Streamlit Community Cloud.

## How It Works

The application uses Huffman compression to convert strings into numbers, which are then mapped to valid Rubik's cube configurations. This creates a unique cube state for each input string.

## Installation & Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/JEdward7777/text_in_rubiks
   cd virtual_rubiks
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## Deployment to Streamlit Community Cloud

1. **Push your code** to a public GitHub repository
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub account** and select your repository
4. **Set the main file path** to `app.py`
5. **Deploy!** Streamlit will automatically install the requirements

### Requirements for Deployment

- `streamlit>=1.28.0`
- `kociemba>=1.2.0` (standard pip package, should work on Community Cloud)

## Usage Guide

### Encoding a String
1. Enter your text in the "Enter string to encode" field
2. Click "Set String"
3. Watch the cube transform to encode your message
4. Note the "Reverse Solution" steps to manually create this state

### Extracting a String
1. With any scrambled cube state
2. Click "Extract String from Cube"
3. See the decoded message (if any)

### Solving the Cube
1. Click "Get Solution" to see the steps to solve the current state
2. Use "Reverse Solution" to see how to reach the current state from solved

## File Structure

```
virtual_rubiks/
├── app.py              # Main Streamlit application
├── cube.py             # Core Rubik's cube logic and string conversion
├── huffy_code.py       # Huffman compression implementation
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── venv/              # Virtual environment (local only)
```

## Technical Details

- **Cube Engine**: Custom 3x3x3 Rubik's cube implementation
- **Solver**: Integration with `kociemba` algorithm for optimal solving
- **Compression**: Huffman coding for efficient string-to-number conversion
- **State Management**: Uses `st.session_state` for persistent cube state
- **Visualization**: CSS-styled colored squares using Streamlit columns

## Limitations

- Maximum string length depends on the Huffman encoding efficiency
- Cube states must be valid and solvable configurations
- Some very long strings may not encode properly (warning system in place)

## Contributing

Feel free to submit issues and pull requests to improve the application!

## License

This project is open source and available under the MIT License.