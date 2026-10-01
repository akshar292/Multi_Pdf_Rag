function SourceCard({ source }) {
    return (
        <div className="source-card">
            <div className="source-title">
                📄 {source.file || source.filename}
            </div>

            {source.page && (
                <div className="source-page">
                    Page {source.page}
                </div>
            )}
        </div>
    );
}

export default SourceCard;