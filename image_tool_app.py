
import streamlit as st
from rembg import remove
from PIL import Image, ImageDraw
import numpy as np
import cv2
import io

st.set_page_config(page_title="Image Background Remover + Object Eraser", layout="centered")

st.title("🧹 Image Background Remover + Object Eraser")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
    st.image(image, caption="Original Image", use_column_width=True)

    if st.button("Remove Background"):
        with st.spinner("Processing..."):
            bg_removed = remove(image)
            st.image(bg_removed, caption="Background Removed", use_column_width=True)

            buf = io.BytesIO()
            bg_removed.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button("Download Background Removed", byte_im, file_name="bg_removed.png")

    st.subheader("🖌️ Object Eraser Tool (Beta)")
    st.write("Click below to enter erase mode. Draw over objects to erase.")

    if st.button("Launch Eraser Tool"):
        canvas_width = 600
        canvas_height = int((image.height / image.width) * canvas_width)

        stroke_width = st.slider("Brush Size", 5, 50, 20)

        # Convert image to numpy array
        img_np = np.array(image.convert("RGB"))

        # Draw on image
        from streamlit_drawable_canvas import st_canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_width=stroke_width,
            stroke_color="#ffffff",
            background_image=Image.fromarray(img_np),
            update_streamlit=True,
            height=canvas_height,
            width=canvas_width,
            drawing_mode="freedraw",
            key="canvas",
        )

        if canvas_result.image_data is not None:
            mask = canvas_result.image_data[:, :, 3]
            erased_img = img_np.copy()
            erased_img[mask > 0] = 255
            erased_pil = Image.fromarray(erased_img)

            st.image(erased_pil, caption="Edited Image", use_column_width=True)

            buf = io.BytesIO()
            erased_pil.save(buf, format="PNG")
            byte_erased = buf.getvalue()
            st.download_button("Download Edited Image", byte_erased, file_name="erased_image.png")
