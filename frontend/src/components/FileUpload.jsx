import { useState } from "react";

import axios from "axios";


const API_URL = "http://127.0.0.1:8000";


function FileUpload() {

    const [files, setFiles] = useState([]);

    const [uploading, setUploading] = useState(false);

    const [results, setResults] = useState([]);


    // =====================================================
    // SELECT FILES
    // =====================================================

    const handleFileChange = (event) => {

        const selectedFiles = Array.from(
            event.target.files
        );

        setFiles(
            selectedFiles
        );

        setResults([]);
    };


    // =====================================================
    // UPLOAD
    // =====================================================

    const uploadFiles = async () => {

        if (!files.length) {

            alert(
                "Please select PDF files first."
            );

            return;
        }


        setUploading(true);

        setResults([]);


        const uploadResults = [];


        for (const file of files) {

            const formData = new FormData();

            formData.append(
                "file",
                file
            );


            try {

                const response =
                    await axios.post(
                        `${API_URL}/upload`,
                        formData,
                        {
                            headers: {
                                "Content-Type":
                                    "multipart/form-data"
                            }
                        }
                    );


                uploadResults.push({

                    filename:
                        file.name,

                    success:
                        true,

                    message:
                        response.data.message,

                    chunks:
                        response.data.chunks

                });

            }

            catch (error) {

                console.error(
                    "Upload error:",
                    error
                );


                uploadResults.push({

                    filename:
                        file.name,

                    success:
                        false,

                    message:
                        error.response?.data?.detail ||
                        "Upload failed."

                });

            }

        }


        setResults(
            uploadResults
        );

        setUploading(false);
    };


    return (

        <section className="upload-card">

            <div className="section-title">

                <span className="icon">
                    📄
                </span>

                <div>

                    <h2>
                        Upload PDF Documents
                    </h2>

                    <p>
                        You can upload multiple PDFs
                        at once.
                    </p>

                </div>

            </div>


            <div className="file-input-wrapper">

                <input
                    type="file"
                    accept=".pdf"
                    multiple
                    onChange={
                        handleFileChange
                    }
                    id="pdf-upload"
                />

                <label htmlFor="pdf-upload">

                    📁 Choose PDF Files

                </label>

            </div>


            {files.length > 0 && (

                <div className="selected-files">

                    <h3>
                        Selected Files
                    </h3>

                    {files.map(
                        (file, index) => (

                            <div
                                className="file-row"
                                key={index}
                            >

                                <span>
                                    📄 {file.name}
                                </span>

                                <span>
                                    {(file.size / 1024).toFixed(1)}
                                    {" "}KB
                                </span>

                            </div>

                        )
                    )}

                </div>

            )}


            <button
                className="upload-button"
                onClick={uploadFiles}
                disabled={
                    uploading ||
                    files.length === 0
                }
            >

                {uploading
                    ? "⏳ Uploading..."
                    : "🚀 Upload & Index PDFs"}

            </button>


            {results.length > 0 && (

                <div className="upload-results">

                    {results.map(
                        (result, index) => (

                            <div
                                className={
                                    result.success
                                        ? "upload-success"
                                        : "upload-error"
                                }
                                key={index}
                            >

                                {result.success
                                    ? "✓"
                                    : "✗"}

                                {" "}

                                <strong>
                                    {result.filename}
                                </strong>

                                <br />

                                <span>
                                    {result.message}
                                </span>

                                {result.success &&
                                    result.chunks && (

                                        <small>
                                            <br />
                                            {result.chunks}
                                            {" "}chunks indexed
                                        </small>

                                    )}

                            </div>

                        )
                    )}

                </div>

            )}

        </section>
    );
}


export default FileUpload;