import streamlit as st
import PyPDF2
import zipfile
import io

# Set up the page
st.set_page_config(page_title="PDF Splitter", page_icon="📄")
st.title("📄 PDF Page Splitter")
st.write("Upload a PDF file, and this app will split it into individual pages and package them into a downloadable ZIP file.")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        # Read the uploaded PDF from memory
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)
        
        st.info(f"File loaded successfully! Total pages: **{num_pages}**")

        # Create a button to trigger the splitting process
        if st.button("Split and Zip PDF"):
            with st.spinner('Splitting pages...'):
                
                # Create an in-memory buffer for the ZIP file
                zip_buffer = io.BytesIO()

                # Open the zip buffer to write
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    
                    # Loop through all pages
                    for i, page in enumerate(pdf_reader.pages):
                        pdf_writer = PyPDF2.PdfWriter()
                        pdf_writer.add_page(page)

                        # Save the single page to an in-memory buffer
                        page_buffer = io.BytesIO()
                        pdf_writer.write(page_buffer)

                        # Write the page buffer to the ZIP file
                        zip_file.writestr(f"page_{i+1}.pdf", page_buffer.getvalue())

                st.success("🎉 PDF split successfully! You can download your ZIP file below.")

                # Provide the download button
                st.download_button(
                    label="⬇️ Download Splitted Pages (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="splitted_pages.zip",
                    mime="application/zip"
                )
                
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
