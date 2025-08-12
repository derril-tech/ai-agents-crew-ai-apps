import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Download, Copy, Check } from 'lucide-react';

const ReportDisplay = ({ report, onCopy }) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(report.report);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
      if (onCopy) onCopy();
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([report.report], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${report.filename || 'sales-report.md'}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!report) return null;

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Generated Report</h2>
        <div className="flex space-x-3">
          <button
            onClick={handleCopy}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
            <span>{copied ? 'Copied!' : 'Copy'}</span>
          </button>
          <button
            onClick={handleDownload}
            className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Download</span>
          </button>
        </div>
      </div>
      
      <div className="bg-white/5 rounded-lg p-6 max-h-96 overflow-y-auto">
        <ReactMarkdown 
          className="prose prose-invert max-w-none"
          components={{
            h1: ({node, ...props}) => <h1 className="text-2xl font-bold text-white mb-4" {...props} />,
            h2: ({node, ...props}) => <h2 className="text-xl font-bold text-white mb-3 mt-6" {...props} />,
            h3: ({node, ...props}) => <h3 className="text-lg font-bold text-white mb-2 mt-4" {...props} />,
            p: ({node, ...props}) => <p className="text-gray-300 mb-3" {...props} />,
            ul: ({node, ...props}) => <ul className="list-disc list-inside text-gray-300 mb-3" {...props} />,
            ol: ({node, ...props}) => <ol className="list-decimal list-inside text-gray-300 mb-3" {...props} />,
            li: ({node, ...props}) => <li className="text-gray-300 mb-1" {...props} />,
            strong: ({node, ...props}) => <strong className="font-bold text-white" {...props} />,
            em: ({node, ...props}) => <em className="italic text-gray-200" {...props} />,
            code: ({node, ...props}) => <code className="bg-gray-800 text-green-400 px-1 py-0.5 rounded text-sm" {...props} />,
            pre: ({node, ...props}) => <pre className="bg-gray-800 text-gray-200 p-4 rounded-lg overflow-x-auto mb-3" {...props} />,
          }}
        >
          {report.report}
        </ReactMarkdown>
      </div>
      
      <div className="mt-6 text-sm text-gray-400">
        <p>Generated for: <span className="text-white">{report.person}</span> at <span className="text-white">{report.company}</span></p>
        <p>Timestamp: <span className="text-white">{report.timestamp}</span></p>
      </div>
    </div>
  );
};

export default ReportDisplay;

