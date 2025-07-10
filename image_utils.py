import os
import shutil
import tempfile
import base64
from PIL import Image
import streamlit as st
import pandas as pd
import webbrowser
from io import BytesIO
from text import HelpText

""" def image_path_and_load():
    # Check if the current row or image option has changed
    if ((st.session_state['last_row_to_edit'] != st.session_state.row_to_edit) or 
        ('last_image_option' not in st.session_state) or 
        (st.session_state['last_image_option'] != st.session_state.image_option) or 
        st.session_state.image_rotation_change):

        # Remember the selected image option
        st.session_state['last_image_option'] = st.session_state.image_option
        st.session_state.last_row_to_edit = st.session_state.row_to_edit

        # Update the image path based on the selected image option
        if st.session_state.image_option == 'Original':
            st.session_state['image_path'] = st.session_state.data_edited.loc[st.session_state.row_to_edit, "path_to_original"]
        elif st.session_state.image_option == 'Cropped':
            st.session_state['image_path'] = st.session_state.data_edited.loc[st.session_state.row_to_edit, "path_to_crop"]
        elif st.session_state.image_option == 'Helper':
            st.session_state['image_path'] = st.session_state.data_edited.loc[st.session_state.row_to_edit, "path_to_helper"]

        # Load the image if the image path is not null
        if pd.notnull(st.session_state['image_path']):
            st.session_state['image'] = apply_image_rotation(Image.open(st.session_state['image_path']))
            st.session_state.relative_path_to_static = image_to_server() """

def image_path_and_load():
    # Check if the current row or image option has changed
    if ((st.session_state['last_row_to_edit'] != st.session_state.row_to_edit) or 
        ('last_image_option' not in st.session_state) or 
        (st.session_state['last_image_option'] != st.session_state.image_option) or 
        st.session_state.image_rotation_change):

        # Debugging information
        print("ROUTING")
        print(f"    new row                --- {st.session_state['last_row_to_edit'] != st.session_state.row_to_edit} --- row {st.session_state.row_to_edit}")
        print(f"    image_option not in st --- {'last_image_option' not in st.session_state}")
        print(f"    image_option changed   --- {st.session_state['last_image_option'] != st.session_state.image_option} --- {st.session_state.image_option}")
        print(f"    image was rotated      --- {st.session_state.image_rotation_change} --- {st.session_state.image_rotation}")

        # Remember the selected image option
        st.session_state['last_image_option'] = st.session_state.image_option
        st.session_state.last_row_to_edit = st.session_state.row_to_edit

        # Update the image path based on the selected image option
        if st.session_state.image_option == 'Original':
            st.session_state['image_path'] = st.session_state.data_edited.loc[st.session_state.row_to_edit, "path_to_original"]
        elif st.session_state.image_option == 'Cropped':
            st.session_state['image_path'] = st.session_state.data_edited.loc[st.session_state.row_to_edit, "path_to_crop"]
        elif st.session_state.image_option == 'Helper':
            st.session_state['image_path'] = st.session_state.data_edited.loc[st.session_state.row_to_edit, "path_to_helper"]

        # Load the image if the image path is not null
        if pd.notnull(st.session_state['image_path']):
            # Handle image rotation if needed
            if st.session_state.image_rotation_change:
                new_img_path = st.session_state['image_path']
                new_img_path_fname = os.path.basename(new_img_path)
                print(f'LOADING IMAGE: {new_img_path_fname}')
                st.session_state['image'] = apply_image_rotation(Image.open(new_img_path))
                st.session_state.image_rotation_change = False
            else:
                st.session_state['image'] = Image.open(st.session_state['image_path'])

            # Save the image to the server and update the relative path
            st.session_state.relative_path_to_static = image_to_server()

def apply_image_rotation(image):
    if st.session_state.image_rotation == 'left':
        return image.rotate(90, expand=True)
    elif st.session_state.image_rotation == 'right':
        return image.rotate(-90, expand=True)
    elif st.session_state.image_rotation == '180':
        return image.rotate(180, expand=True)
    else:
        return image

""" def image_to_server():
    image_path = st.session_state['image_path']
    if 'image_rotation' in st.session_state and st.session_state.image_rotation in ['left', 'right', '180']:
        # Save the rotated image to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_path)[1])
        st.session_state['image'].save(temp_file.name)
        image_path = temp_file.name  # Update image_path to point to the rotated image
        st.session_state['image_path'] = image_path

    # Continue with the existing logic to determine the destination path
    if st.session_state.image_option == 'Original':
        static_image_path = os.path.join('static_og', os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(st.session_state.static_folder_path_o, os.path.basename(image_path)))
    elif st.session_state.image_option == 'Cropped':
        static_image_path = os.path.join('static_cr', os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(st.session_state.static_folder_path_c, os.path.basename(image_path)))
    elif st.session_state.image_option == 'Helper':
        static_image_path = os.path.join('static_h', os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(st.session_state.static_folder_path_h, os.path.basename(image_path)))

    # Generate and return the relative path to the static directory
    relative_path_to_static = os.path.relpath(static_image_path, st.session_state.current_dir).replace('\\', '/')
    return relative_path_to_static """

def image_to_server():
    """
    Save the image to the server and update the relative path.
    Handles image rotation and saves rotated images to a temporary file.
    """
    image_path = st.session_state['image_path']
    print(f"Processing image: {image_path}")

    # Handle image rotation if applicable
    if 'image_rotation' in st.session_state and st.session_state.image_rotation in ['left', 'right', '180']:
        print(f"Applying rotation: {st.session_state.image_rotation}")
        # Save the rotated image to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_path)[1])
        st.session_state['image'].save(temp_file.name)
        image_path = temp_file.name  # Update image_path to point to the rotated image
        st.session_state['image_path'] = image_path
        st.session_state.image_rotation_change = False  # Reset rotation change flag

    # Determine the destination path based on the image option
    if st.session_state.image_option == 'Original':
        static_image_path = os.path.join('static_og', os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(st.session_state.static_folder_path_o, os.path.basename(image_path)))
    elif st.session_state.image_option == 'Cropped':
        static_image_path = os.path.join('static_cr', os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(st.session_state.static_folder_path_c, os.path.basename(image_path)))
    elif st.session_state.image_option == 'Helper':
        static_image_path = os.path.join('static_h', os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(st.session_state.static_folder_path_h, os.path.basename(image_path)))

    # Generate and return the relative path to the static directory
    relative_path_to_static = os.path.relpath(static_image_path, st.session_state.current_dir).replace('\\', '/')
    print(f"Image added to server: {relative_path_to_static}")
    return relative_path_to_static

""" def display_image_options_buttons(relative_path_to_static):
    # Define the Zoom link
    link = f'http://localhost:8000/{relative_path_to_static}'

    # Add buttons for image options
    if st.button('Zoom', use_container_width=True, help="Open the current image in a new tab. Can zoom in."):
        webbrowser.open_new_tab(link) """

def display_image_options_buttons(relative_path_to_static, zoom_1=None, zoom_2=None, zoom_3=None, zoom_4=None):
    """
    Display buttons for different image options.
    The number and type of buttons displayed depends on st.session_state.use_extra_image_options.
    """
    # Define the Zoom link
    link = f'http://localhost:8000/{relative_path_to_static}'
    
    # Track the current image option
    current_image = st.session_state.image_option

    # Check if extra image options are enabled
    if st.session_state.use_extra_image_options:
        if zoom_1:
            with zoom_1:
                if st.button('Original', use_container_width=True):
                    st.session_state.image_option = 'Original'
        if zoom_2:
            with zoom_2:
                if st.button('Zoom', use_container_width=True):
                    webbrowser.open_new_tab(link)
        if zoom_3:
            with zoom_3:
                if st.button('Toggle Fitted', use_container_width=True):
                    st.session_state.is_fitted_image = not st.session_state.is_fitted_image
                    st.session_state.set_image_size = 'Fitted' if st.session_state.is_fitted_image else st.session_state.set_image_size_previous
        if st.session_state.tool_access.get('ocr') and zoom_4:
            with zoom_4:
                if st.button('Collage', use_container_width=True):
                    st.session_state.image_option = 'Cropped'
    else:
        if zoom_1:
            with zoom_1:
                if st.button('Original', use_container_width=True, help="View the full specimen image"):
                    st.session_state.image_option = 'Original'
        if zoom_2:
            with zoom_2:
                if st.button('Zoom', use_container_width=True, help="Open the current image in a new tab. Can zoom in."):
                    webbrowser.open_new_tab(link)
        if zoom_3:
            with zoom_3:
                if st.button('Collage', use_container_width=True, help="View the LeafMachine2 label collage. Shows all text ONLY."):
                    st.session_state.image_option = 'Cropped'
        if st.session_state.tool_access.get('ocr') and zoom_4:
            with zoom_4:
                if st.button('OCR', use_container_width=True):
                    st.session_state.image_option = 'Helper'

    # Check if the image option has changed
    last_image_option = st.session_state.image_option
    if current_image != last_image_option:
        st.rerun()

###############################################################
###################### Image Handling #########################
###############################################################
""" def image_path_and_load():
    # Check if the current row or image option has changed
    if ((st.session_state['last_row_to_edit'] != st.session_state.row_to_edit) or 
        ('last_image_option' not in st.session_state) or 
        (st.session_state['last_image_option'] != st.session_state.image_option) or 
        st.session_state.image_rotation_change):

        print("ROUTING")
        print(f"    new row                --- {st.session_state['last_row_to_edit'] != st.session_state.row_to_edit} --- row {st.session_state.row_to_edit}")
        print(f"    image_option not in st --- {'last_image_option' not in st.session_state}")
        print(f"    image_option changed   --- {st.session_state['last_image_option'] != st.session_state.image_option} --- {st.session_state.image_option}")
        print(f"    image was rotated      --- {st.session_state.image_rotation_change} --- {st.session_state.image_rotation}")

        # Remember the selected image option
        st.session_state['last_image_option'] = st.session_state.image_option
        st.session_state.last_row_to_edit = st.session_state.row_to_edit

        # Update the image path based on the selected image option
        if st.session_state.image_option == 'Original':
            st.session_state['image_path'] = st.session_state.data_edited.loc[st.session_state.row_to_edit, "path_to_original"]
            st.session_state['image'] = Image.open(st.session_state['image_path'])
            st.session_state.relative_path_to_static = image_to_server()
        elif st.session_state.image_option == 'Cropped':
            st.session_state['image_path'] = st.session_state.data_edited.loc[st.session_state.row_to_edit, "path_to_crop"]
            st.session_state['image'] = Image.open(st.session_state['image_path'])
            st.session_state.relative_path_to_static = image_to_server()
        elif st.session_state.image_option == 'Helper':
            st.session_state['image_path'] = st.session_state.data_edited.loc[st.session_state.row_to_edit, "path_to_helper"]
            st.session_state['image'] = Image.open(st.session_state['image_path'])
            st.session_state.relative_path_to_static = image_to_server()

        # Load the image if the image path is not null
        if st.session_state.image_rotation_change:
            if pd.notnull(st.session_state['image_path']):
                new_img_path = st.session_state['image_path']
                new_img_path_fname = os.path.basename(new_img_path)
                print(f'LOADING IMAGE: {new_img_path_fname}')
                # st.session_state['image_path'] = new_img_path
                st.session_state['image'] = apply_image_rotation(Image.open(new_img_path))
            st.session_state.image_rotation_change = False
            st.session_state.relative_path_to_static = image_to_server() """
           
""" def image_to_server():

    image_path = st.session_state['image_path']
    print(image_path)
    if 'image_rotation' in st.session_state and st.session_state.image_rotation in ['left', 'right', '180']:

        # Save the rotated image to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_path)[1])
        st.session_state['image'].save(temp_file.name)
        image_path = temp_file.name  # Update image_path to point to the rotated image
        st.session_state['image_path'] = image_path
        # st.session_state.image_rotation_change = False
    
    # Continue with the existing logic to determine the destination path
    if st.session_state.image_option == 'Original':
        static_image_path = os.path.join('static_og', os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(st.session_state.static_folder_path_o, os.path.basename(image_path)))
    elif st.session_state.image_option == 'Cropped':
        static_image_path = os.path.join('static_cr', os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(st.session_state.static_folder_path_c, os.path.basename(image_path)))
    elif st.session_state.image_option == 'Helper':
        static_image_path = os.path.join('static_h', os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(st.session_state.static_folder_path_h, os.path.basename(image_path)))
    
    # Generate and print the relative path to the static directory
    relative_path_to_static = os.path.relpath(static_image_path, st.session_state.current_dir).replace('\\', '/')
    print(f"Adding to Zoom image server: {relative_path_to_static}")
    return relative_path_to_static """

""" def display_image_options_buttons(relative_path_to_static, zoom_1, zoom_2, zoom_3, zoom_4):
 
    # Define the Zoom link
    link = f'http://localhost:8000/{relative_path_to_static}'
    
    current_image = st.session_state.image_option
    if st.session_state.use_extra_image_options:
        with zoom_1:
            if st.button('Original', use_container_width=True):
                st.session_state.image_option = 'Original'
        with zoom_2:
            if st.button('Zoom', use_container_width=True):
                webbrowser.open_new_tab(link)
        with zoom_3:
            if st.button('Toggle Fitted', use_container_width=True):
                st.session_state.is_fitted_image = not st.session_state.is_fitted_image
                st.session_state.set_image_size = 'Fitted' if st.session_state.is_fitted_image else st.session_state.set_image_size_previous
        if st.session_state.tool_access.get('ocr'):
            with zoom_4:
                if st.button('Collage', use_container_width=True):
                    st.session_state.image_option = 'Cropped'
    else:
        with zoom_1:
            if st.button('Original', use_container_width=True, help="View the full specimen image"):
                st.session_state.image_option = 'Original'
        with zoom_2:
            if st.button('Zoom', use_container_width=True, help="Open the current image in a new tab. Can zoom in."):
                webbrowser.open_new_tab(link)
        with zoom_3:
            if st.button('Collage', use_container_width=True, help="View the LeafMachine2 label collage. Shows all text ONLY."):
                st.session_state.image_option = 'Cropped'
        if st.session_state.tool_access.get('ocr'):
            with zoom_4:
                if st.button('OCR', use_container_width=True):
                    st.session_state.image_option = 'Helper'
    last_image_option = st.session_state.image_option
    if current_image != last_image_option:
        st.rerun() """
# Function to convert image to base64
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def display_image_rotation_buttons(r1, r2, r3, r4):
    st.session_state.image_rotation_previous
    with r1:
        if st.button(':arrow_right_hook:', use_container_width=True,help="Rotate image 90 degrees counterclockwise"):
            st.session_state.image_rotation = 'left'
            if st.session_state.image_rotation_previous != st.session_state.image_rotation:
                st.session_state.image_rotation_previous = st.session_state.image_rotation
                st.session_state.image_rotation_change = True
                st.rerun()

    with r2:
        if st.button(':leftwards_arrow_with_hook:', use_container_width=True,help="Rotate image 90 degrees clockwise"):
            st.session_state.image_rotation = 'right'
            if st.session_state.image_rotation_previous != st.session_state.image_rotation:
                st.session_state.image_rotation_previous = st.session_state.image_rotation
                st.session_state.image_rotation_change = True
                st.rerun()
    with r3:
        if st.button(':arrow_double_down:', use_container_width=True,help="Rotate image 180 degrees"):
            st.session_state.image_rotation = '180'
            if st.session_state.image_rotation_previous != st.session_state.image_rotation:
                st.session_state.image_rotation_previous = st.session_state.image_rotation
                st.session_state.image_rotation_change = True
                st.rerun()
    with r4:
        if st.button(':arrow_double_up:', use_container_width=True,help="Normal"):
            st.session_state.image_rotation = '0'
            if st.session_state.image_rotation_previous != st.session_state.image_rotation:
                st.session_state.image_rotation_previous = st.session_state.image_rotation
                st.session_state.image_rotation_change = True
                st.rerun()


def display_scrollable_image(con_image):
    """
    Display the image from st.session_state in a scrollable container.
    The width and height of the container are determined by st.session_state values.
    """
    # Initialize the container
    with con_image:
        display_scrollable_image_method()


def display_scrollable_image_method():

    # Determine the desired width based on st.session_state.set_image_size
    if st.session_state.set_image_size == "Auto Width":
        st.image(st.session_state['image'], caption=st.session_state['image_path'], use_container_width=True)
        return

    if st.session_state.set_image_size == "Custom":
        image_width = st.session_state.set_image_size_px
    elif st.session_state.set_image_size == "Large":
        image_width = 1500
    elif st.session_state.set_image_size == "Medium":
        image_width = 1100
    elif st.session_state.set_image_size == "Small":
        image_width = 800
    elif st.session_state.set_image_size == "Fitted":
        image_width = 600
    else:
        image_width = st.session_state.set_image_size_px  # For use_container_width=True

    # Convert the image to base64
    base64_image = image_to_base64(st.session_state['image'])

    # Embed the image with the determined width in the custom div
    img_html = f"""
    <div class='scrollable-image-container'>
        <img src='data:image/jpeg;base64,{base64_image}' alt='Image' style='width:{image_width}px'>
    </div>
    """

    # The CSS to make this container scrollable, with dynamic height based on st.session_state.set_image_size_pxh
    css = f"""
    <style>
        .scrollable-image-container {{
            overflow: auto;
            height: {st.session_state.set_image_size_pxh}vh;
            width: 70vw;
            text-align: left;
            margin-left: 0;
        }}
    </style>
    """
    css_img_left = f"""
    <style>
        .scrollable-image-container {{
            overflow: auto;
            height: {st.session_state.set_image_size_pxh}vh;
            width: 70vw;
            direction: rtl;
            text-align: left;
            margin-left: 0;
        }}
    </style>
    """

    is_img_left = False
    pts = st.session_state.image_fill.split(" ")
    if "Left" in pts:
        is_img_left = True

    if is_img_left:
        st.markdown(css_img_left, unsafe_allow_html=True)
    else:
        # Apply the CSS and then the image
        st.markdown(css, unsafe_allow_html=True)
    st.markdown(img_html, unsafe_allow_html=True)



def display_help():
    st.write('---')
    st.subheader("Help")
    with st.expander(":grey_question: Image Buttons"):
        st.write("**Buttons**")
        st.write(HelpText.help_btns)
    with st.expander(":grey_question: Tool Hints"):
        st.write("**Buttons**")
        st.write(HelpText.help_form_btns)
        st.write("**Tool Hints**")
        st.write(HelpText.help_form)
    with st.expander(":grey_question: Specimen Record"):
        st.write("**Specimen Record**")
        st.write(HelpText.help_specimen)
    with st.expander(":grey_question: Enabling/Hiding Tools"):
        st.write("**Enabling/Hiding Tools**")
        st.write(HelpText.help_hide_tools)
    with st.expander(":grey_question: Categories"):
        st.write("**Categories**")
        st.write(HelpText.help_categories)
    with st.expander(":grey_question: Other"):
        st.write("**World Flora Online Badge**")
        st.write(HelpText.help_WFO_badge)
        st.write("**Categories**")
        st.write(HelpText.help_WFO_badge)