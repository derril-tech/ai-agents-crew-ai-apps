// Test the regex logic
const testProjectName = "AI-Powered Code Review & Refactoring Assistant"

console.log('Original:', testProjectName)
console.log('Step 1 (toLowerCase):', testProjectName.toLowerCase())
console.log('Step 2 (replace &):', testProjectName.toLowerCase().replace(/&/g, 'and'))
console.log('Step 3 (remove special chars):', testProjectName.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s]+/g, ''))
console.log('Step 4 (spaces to dashes):', testProjectName.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s]+/g, '').replace(/\s+/g, '-'))
console.log('Step 5 (trim dashes):', testProjectName.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, ''))

const finalResult = testProjectName.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '')
console.log('Final result:', finalResult)
console.log('Expected:', 'ai-powered-code-review-and-refactoring-assistant')
console.log('Match:', finalResult === 'ai-powered-code-review-and-refactoring-assistant')
