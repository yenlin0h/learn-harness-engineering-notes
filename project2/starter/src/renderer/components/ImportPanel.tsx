import React, { useState } from 'react';

interface Props {
  onImport: (filePath: string) => Promise<void>;
}

export function ImportPanel({ onImport }: Props) {
  const [error, setError] = useState<string | null>(null);

  const handleBrowse = async () => {
    setError(null);
    const filePath = await window.knowledgeBase.documents.selectImportFile();
    if (!filePath) return;
    try {
      await onImport(filePath);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Import failed');
    }
  };

  return (
    <div style={{
      padding: '20px',
      background: '#16213e',
      borderRadius: '6px',
      border: '1px dashed #0f3460',
      textAlign: 'center',
      color: '#888',
    }}>
      <div style={{ fontSize: '14px', marginBottom: '8px' }}>Import Documents</div>
      <div style={{ fontSize: '12px' }}>
        Choose a file to import.
        <br />
        Supported: .txt, .md files
      </div>
      <button
        onClick={handleBrowse}
        style={{
          marginTop: '10px',
          padding: '6px 14px',
          background: '#533483',
          color: '#fff',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '13px',
        }}
      >
        Choose File
      </button>
      {error && (
        <div style={{ marginTop: '10px', color: '#d9534f', fontSize: '12px' }}>{error}</div>
      )}
    </div>
  );
}
