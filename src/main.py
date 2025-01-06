from textnode import *

def main():
    # Create a TextNode object with dummy values
    text_node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    
    # Print the object to verify its string representation
    print(text_node)

# Entry point
if __name__ == "__main__":
    main()

