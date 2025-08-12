const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ status: 'API is running', timestamp: new Date().toISOString() });
});

// Main endpoint to generate sales pitch
app.post('/api/generate-sales-pitch', async (req, res) => {
    const { person, company } = req.body;
    
    // Validate input
    if (!person || !company) {
        return res.status(400).json({
            success: false,
            error: 'Both person and company are required'
        });
    }
    
    try {
        // Set up the Python script execution
        const pythonScript = path.join(__dirname, '..', 'backend', 'main.py');
        
        // Check if Python script exists
        if (!fs.existsSync(pythonScript)) {
            return res.status(500).json({
                success: false,
                error: 'Python script not found. Please ensure the backend is properly set up.'
            });
        }
        
        // Spawn Python process
        const pythonProcess = spawn('python', [pythonScript, person, company], {
            cwd: path.join(__dirname, '..', 'backend')
        });
        
        let outputData = '';
        let errorData = '';
        
        // Collect stdout data
        pythonProcess.stdout.on('data', (data) => {
            outputData += data.toString();
        });
        
        // Collect stderr data
        pythonProcess.stderr.on('data', (data) => {
            errorData += data.toString();
        });
        
        // Handle process completion
        pythonProcess.on('close', (code) => {
            if (code === 0) {
                try {
                    // Try to parse JSON response from Python script
                    const lastJsonLine = outputData.split('\n').reverse().find(line => {
                        try {
                            JSON.parse(line);
                            return true;
                        } catch {
                            return false;
                        }
                    });
                    
                    if (lastJsonLine) {
                        const result = JSON.parse(lastJsonLine);
                        res.json(result);
                    } else {
                        // Fallback: return raw output if JSON parsing fails
                        res.json({
                            success: true,
                            report: outputData,
                            person,
                            company,
                            timestamp: new Date().toISOString()
                        });
                    }
                } catch (parseError) {
                    res.status(500).json({
                        success: false,
                        error: 'Failed to parse Python script output',
                        details: parseError.message,
                        rawOutput: outputData
                    });
                }
            } else {
                res.status(500).json({
                    success: false,
                    error: 'Python script execution failed',
                    exitCode: code,
                    stderr: errorData,
                    stdout: outputData
                });
            }
        });
        
        // Handle process errors
        pythonProcess.on('error', (error) => {
            res.status(500).json({
                success: false,
                error: 'Failed to start Python script',
                details: error.message
            });
        });
        
        // Set timeout (5 minutes)
        setTimeout(() => {
            pythonProcess.kill();
            res.status(408).json({
                success: false,
                error: 'Request timeout - Python script execution took too long'
            });
        }, 300000);
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: 'Internal server error',
            details: error.message
        });
    }
});

// Endpoint to get list of generated reports
app.get('/api/reports', (req, res) => {
    try {
        const outputsDir = path.join(__dirname, '..', 'backend', 'outputs');
        
        if (!fs.existsSync(outputsDir)) {
            return res.json({ reports: [] });
        }
        
        const files = fs.readdirSync(outputsDir)
            .filter(file => file.endsWith('.md'))
            .map(file => {
                const filePath = path.join(outputsDir, file);
                const stats = fs.statSync(filePath);
                return {
                    filename: file,
                    created: stats.birthtime,
                    modified: stats.mtime,
                    size: stats.size
                };
            })
            .sort((a, b) => new Date(b.created) - new Date(a.created));
        
        res.json({ reports: files });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to retrieve reports',
            details: error.message
        });
    }
});

// Endpoint to download a specific report
app.get('/api/reports/:filename', (req, res) => {
    try {
        const filename = req.params.filename;
        const filePath = path.join(__dirname, '..', 'backend', 'outputs', filename);
        
        if (!fs.existsSync(filePath)) {
            return res.status(404).json({
                success: false,
                error: 'Report not found'
            });
        }
        
        const content = fs.readFileSync(filePath, 'utf8');
        res.json({
            success: true,
            filename,
            content
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: 'Failed to read report',
            details: error.message
        });
    }
});

// Serve static files from React build (for production)
if (process.env.NODE_ENV === 'production') {
    app.use(express.static(path.join(__dirname, '..', 'frontend', 'build')));
    
    app.get('*', (req, res) => {
        res.sendFile(path.join(__dirname, '..', 'frontend', 'build', 'index.html'));
    });
}

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Sales Pitch Assistant API running on port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/api/health`);
    console.log(`🤖 Generate sales pitch: POST http://localhost:${PORT}/api/generate-sales-pitch`);
});