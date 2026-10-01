import FileUpload from "./components/FileUpload";

import ChatBox from "./components/ChatBox";


function App() {

  return (

    <div className="app">

      <header className="header">

        <div className="header-content">

          <div className="logo">
            📚
          </div>

          <div>

            <h1>
              Multi-PDF RAG Assistant
            </h1>

            <p>
              Chat with multiple PDF documents
              using AI
            </p>

          </div>

        </div>

      </header>


      <main className="container">

        <section className="hero">

          <h2>
            Ask Questions From Your PDFs
          </h2>

          <p>
            Upload multiple PDF documents and
            ask questions using semantic search,
            LangGraph and Groq AI.
          </p>

        </section>


        <FileUpload />


        <ChatBox />

      </main>


      <footer>

        <p>
          Multi-PDF RAG • LangGraph • ChromaDB • Groq
        </p>

      </footer>

    </div>
  );
}


export default App;