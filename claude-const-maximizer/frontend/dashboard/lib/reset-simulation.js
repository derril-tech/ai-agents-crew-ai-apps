// Reset all simulation states
const fs = require('fs');
const path = require('path');

// Reset pipeline-todos.json
const pipelineTodosPath = path.join(__dirname, 'pipeline-todos.json');
fs.writeFileSync(pipelineTodosPath, '{}', 'utf-8');
console.log('✅ Reset pipeline-todos.json');

// Reset pipeline_status.json if it exists
const pipelineStatusPath = path.join(__dirname, '../../backend/pipeline_status.json');
if (fs.existsSync(pipelineStatusPath)) {
  fs.writeFileSync(pipelineStatusPath, '{}', 'utf-8');
  console.log('✅ Reset pipeline_status.json');
} else {
  console.log('ℹ️  pipeline_status.json does not exist');
}

console.log('🔄 All simulation states have been reset!');


