import { useState } from "react";

import axios from "axios";


const API_URL = "http://127.0.0.1:8000";


function ChatBox() {

    const [question, setQuestion] =
        useState("");

    const [answer, setAnswer] =
        useState("");

    const [sources, setSources] =
        useState([]);

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState("");


    // =====================================================
    // ASK QUESTION
    // =====================================================

    const askQuestion = async () => {

        if (!question.trim()) {
            return;
        }


        setLoading(true);

        setError("");

        setAnswer("");

        setSources([]);


        try {

            const response =
                await axios.post(
                    `${API_URL}/ask`,
                    {
                        question:
                            question.trim()
                    }
                );


            console.log(
                "API RESPONSE:",
                response.data
            );


            const data =
                response.data;


            // --------------------------------------------------
            // CLEAN ANSWER
            // --------------------------------------------------

            let cleanAnswer = "";


            if (
                typeof data.answer ===
                "string"
            ) {

                cleanAnswer =
                    data.answer;

            }


            else if (
                Array.isArray(
                    data.answer
                )
            ) {

                cleanAnswer =
                    data.answer
                        .filter(
                            (item) =>
                                item.type ===
                                "text"
                        )
                        .map(
                            (item) =>
                                item.text
                        )
                        .join("\n\n");

            }


            else if (
                data.answer &&
                typeof data.answer.text ===
                "string"
            ) {

                cleanAnswer =
                    data.answer.text;

            }


            setAnswer(
                cleanAnswer ||
                "No answer generated."
            );


            // --------------------------------------------------
            // SOURCES
            // --------------------------------------------------

            if (
                Array.isArray(
                    data.sources
                )
            ) {

                setSources(
                    data.sources
                );

            }

        }


        catch (error) {

            console.error(
                "ASK ERROR:",
                error
            );


            setError(
                error.response?.data?.detail ||
                error.message ||
                "Something went wrong."
            );

        }


        finally {

            setLoading(false);

        }

    };


    // =====================================================
    // ENTER KEY
    // =====================================================

    const handleKeyDown = (
        event
    ) => {

        if (
            event.key ===
            "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            askQuestion();

        }

    };


    return (

        <section className="chat-card">

            <div className="section-title">

                <span className="icon">
                    💬
                </span>

                <div>

                    <h2>
                        Ask Questions
                    </h2>

                    <p>
                        Ask questions about
                        your uploaded PDFs.
                    </p>

                </div>

            </div>


            {/* QUESTION */}

            <textarea

                value={question}

                onChange={(event) =>
                    setQuestion(
                        event.target.value
                    )
                }

                onKeyDown={
                    handleKeyDown
                }

                placeholder={
                    "Example: What is TF-IDF?"
                }

                rows={5}

            />


            {/* BUTTON */}

            <button

                className="ask-button"

                onClick={
                    askQuestion
                }

                disabled={
                    loading ||
                    !question.trim()
                }

            >

                {loading
                    ? "🤔 Thinking..."
                    : "🤖 Ask AI"}

            </button>


            {/* ERROR */}

            {error && (

                <div className="error">

                    ❌ {error}

                </div>

            )}


            {/* LOADING */}

            {loading && (

                <div className="loading">

                    🔍 Searching documents...

                    <br />

                    🤖 Generating answer...

                </div>

            )}


            {/* ANSWER */}

            {answer &&
                !loading && (

                    <div className="answer-section">

                        <h3>
                            🤖 Answer
                        </h3>

                        <div className="answer">

                            {answer}

                        </div>

                    </div>

                )}


            {/* SOURCES */}

            {sources.length > 0 &&
                !loading && (

                    <div className="sources-section">

                        <h3>
                            📚 Sources
                        </h3>


                        {sources.map(
                            (source, index) => (

                                <div
                                    className="source-item"
                                    key={index}
                                >

                                    <div>

                                        📄{" "}

                                        <strong>
                                            {
                                                source.file ||
                                                source.filename ||
                                                "Document"
                                            }
                                        </strong>

                                    </div>


                                    <span>

                                        Page{" "}

                                        {
                                            source.page
                                        }

                                    </span>

                                </div>

                            )
                        )}

                    </div>

                )}

        </section>
    );
}


export default ChatBox;