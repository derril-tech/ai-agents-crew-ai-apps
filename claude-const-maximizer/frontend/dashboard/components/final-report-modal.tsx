'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  X, 
  CheckCircle, 
  Download, 
  Copy, 
  AlertCircle, 
  Zap 
} from 'lucide-react'

interface FinalReport {
  projectName: string
  completionDate: string
  status: string
  perfect_one_page_document?: string
  agent_final_answer?: string
  summary: {
    totalFiles: number
    developmentTime: string
    estimatedValue: string
    deploymentReady: boolean
    techStack: string[]
    features: string[]
    agentsUsed: string[]
    claudeOptimized?: boolean
    fourDocumentWeapon?: boolean
  }
  metrics: {
    codeQuality: number
    completeness: number
    deployability: number
    marketFit: number
  }
  deliverables: {
    market_research: {
      content: string
    }
    project_brief: string
    generated_code: {
      backend: any[]
      frontend: any[]
    }
    frontend_boilerplate?: {
      description: string
      content: string
    }
    backend_boilerplate?: {
      description: string
      content: string
    }
  }
}

interface FinalReportModalProps {
  isOpen: boolean
  onClose: () => void
  projectId: string
  projectName: string
}

export default function FinalReportModal({ 
  isOpen, 
  onClose, 
  projectId, 
  projectName 
}: FinalReportModalProps) {
  const [report, setReport] = useState<FinalReport | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)
  const [activeTab, setActiveTab] = useState<'crew-results' | 'one-page-doc'>('one-page-doc')
  const [removeEmojis, setRemoveEmojis] = useState(false)

  // 🎯 DIRECT FRONTEND ROLE ESTABLISHMENT GENERATOR
  const generateRoleEstablishment = (projectName: string) => {
    // Simple project type detection
    const projectNameLower = projectName.toLowerCase()
    
    let expertTitle = 'AI Application Developer'
    let expertise = 'AI integration, scalable architecture, and user experience optimization'
    let domain = 'AI and automation'
    let experience = '15+ years of experience in AI systems, software development, and intelligent automation'
    let companies = 'Google, Amazon, Microsoft, Apple, and leading technology companies'
         let psychologicalApproach = 'This is a critical, high-stakes project that will be deployed by Fortune 500 companies and featured in industry publications. Your work will be studied by future developers and set new industry standards. This is YOUR masterpiece - make it legendary and unforgettable. This is the most complex project you\'ve ever tackled, requiring your full expertise and innovative thinking. Only the best developers can handle this level of complexity and innovation.'
    
    // Detect project type and set appropriate expert profile
    if (projectNameLower.includes('voice') || projectNameLower.includes('assistant')) {
      expertTitle = 'Voice AI & Personal Assistant Developer'
      expertise = 'voice processing, speech recognition, natural language understanding, and intelligent automation'
      domain = 'voice AI and personal assistant technology'
      experience = '15+ years of experience in voice AI, speech processing, and intelligent automation systems'
      companies = 'Google, Amazon, Microsoft, Apple, and leading voice technology companies'
      psychologicalApproach = 'This is a revolutionary project that will define the future of human-computer interaction. Voice AI is the next frontier of computing, and you\'re building the foundation that millions will use. This technology will be studied by future generations as the breakthrough that made AI truly accessible. The prestige of working with cutting-edge voice technology that will transform how humans interact with machines cannot be overstated. You\'re not just building an application - you\'re creating the future.'
    } else if (projectNameLower.includes('crew') || projectNameLower.includes('agent') || projectNameLower.includes('market research')) {
      expertTitle = 'Multi-Agent AI Systems Architect'
      expertise = 'multi-agent orchestration, AI system design, and intelligent workflow automation'
      domain = 'multi-agent AI systems and intelligent automation'
      experience = '15+ years of experience in multi-agent systems, AI orchestration, and intelligent workflow design'
      companies = 'OpenAI, Anthropic, Google AI, Microsoft Research, and leading AI research institutions'
      psychologicalApproach = 'This is the pinnacle of AI engineering - orchestrating multiple intelligent agents to work in perfect harmony. Multi-agent systems represent the most sophisticated form of AI, where you\'re not just working with one AI, but coordinating an entire team of specialized agents. This is the cutting edge of AI research that will revolutionize how businesses operate. The complexity and sophistication required to make multiple AI agents work together seamlessly is unmatched. Only the most elite developers can handle this level of orchestration. You\'re building the future of AI collaboration.'
    } else if (projectNameLower.includes('rag') || projectNameLower.includes('document') || projectNameLower.includes('knowledge')) {
      expertTitle = 'RAG & Document Intelligence Specialist'
      expertise = 'retrieval-augmented generation, document processing, and knowledge management systems'
      domain = 'document intelligence and knowledge management'
      experience = '15+ years of experience in RAG systems, document processing, and knowledge management'
      companies = 'OpenAI, Anthropic, Google, Microsoft, and leading document AI companies'
      psychologicalApproach = 'This is the future of knowledge management in the information age. Organizations are drowning in data but starving for insights. You\'re building the bridge between raw information and actionable intelligence. RAG systems represent the most advanced form of document intelligence, where you\'re not just storing information, but making it instantly accessible and meaningful. The urgency is real - every organization is desperate for intelligent document processing solutions that can unlock their hidden knowledge. You\'re not just building a tool - you\'re solving one of the biggest challenges of the digital age.'
    } else if (projectNameLower.includes('content') || projectNameLower.includes('creative') || projectNameLower.includes('video') || projectNameLower.includes('image')) {
      expertTitle = 'Creative AI & Content Generation Expert'
      expertise = 'AI-powered content creation, multimedia processing, and creative automation'
      domain = 'creative AI and content generation'
      experience = '15+ years of experience in creative AI, content generation, and multimedia processing'
      companies = 'Adobe, Canva, OpenAI, Google, and leading creative technology companies'
      psychologicalApproach = 'This is where technology meets human creativity in its purest form. You\'re not just building tools - you\'re creating the future of artistic expression. Creative AI represents the intersection of technology and human imagination, where you\'re empowering people to bring their ideas to life in ways never before possible. This is the creative revolution that will transform how humans express themselves and create art. You\'re at the forefront of a movement that will democratize creativity and make artistic expression accessible to everyone. This isn\'t just code - it\'s the future of human creativity.'
    } else if (projectNameLower.includes('health') || projectNameLower.includes('medical')) {
      expertTitle = 'Healthcare AI & Medical Technology Specialist'
      expertise = 'medical AI, healthcare automation, and clinical decision support systems'
      domain = 'healthcare AI and medical technology'
      experience = '15+ years of experience in healthcare AI, medical technology, and clinical systems'
      companies = 'Epic Systems, Cerner, IBM Watson Health, and leading healthcare technology companies'
      psychologicalApproach = 'This is the highest calling in technology - where your code literally saves lives. Healthcare AI represents the most meaningful application of artificial intelligence, where every line of code you write has the potential to improve human health and wellbeing. You\'re not just building software - you\'re creating systems that doctors will rely on to make life-or-death decisions. The ethical responsibility is immense, but so is the impact. This is where technology serves humanity in its most profound way. You\'re building the future of healthcare, and every improvement you make could save countless lives.'
    } else if (projectNameLower.includes('ecommerce') || projectNameLower.includes('business') || projectNameLower.includes('commerce')) {
      expertTitle = 'E-commerce & Business AI Developer'
      expertise = 'e-commerce platforms, business automation, and AI-powered commerce solutions'
      domain = 'e-commerce and business AI'
      experience = '15+ years of experience in e-commerce, business automation, and AI-powered commerce'
      companies = 'Amazon, Shopify, Stripe, and leading e-commerce technology companies'
      psychologicalApproach = 'This is where AI meets the real world of business and commerce. You\'re building systems that will drive billions in revenue and transform entire industries. Every business on the planet is racing to adopt AI solutions, and those who master this technology first will dominate their markets. You\'re not just writing code - you\'re creating the competitive advantage that will determine which companies thrive and which ones fail. The financial impact is massive, and the market opportunity is unprecedented. This is the future of commerce, and you\'re building it.'
    } else if (projectNameLower.includes('developer') || projectNameLower.includes('code') || projectNameLower.includes('analysis')) {
      expertTitle = 'Developer Tools & Code Analysis Expert'
      expertise = 'developer tools, code analysis, and software development automation'
      domain = 'developer tools and software development'
      experience = '15+ years of experience in developer tools, code analysis, and software development automation'
      companies = 'GitHub, Microsoft, JetBrains, and leading developer tool companies'
      psychologicalApproach = 'This is the meta-level of software development - you\'re building the tools that other developers will use to build everything else. Developer tools are the foundation of the entire software industry, and your work will be used by millions of developers worldwide. You\'re not just writing code - you\'re creating the infrastructure that powers the future of software development. Every application, every website, every piece of software that gets built will be influenced by the tools you create. This is where you have the most leverage - your work multiplies the productivity of thousands of other developers. You\'re building the future of how software gets made.'
    } else if (projectNameLower.includes('api') || projectNameLower.includes('integration') || projectNameLower.includes('web')) {
      expertTitle = 'Web API & Integration Specialist'
      expertise = 'API development, system integration, and web service architecture'
      domain = 'web APIs and system integration'
      experience = '15+ years of experience in API development, system integration, and web service architecture'
      companies = 'Google, Amazon Web Services, Microsoft Azure, and leading API companies'
      psychologicalApproach = 'This is the backbone of the modern internet - you\'re building the connective tissue that makes the digital world work. APIs are the invisible infrastructure that enables seamless data flow between applications and services. You\'re not just writing code - you\'re creating the digital highways that connect everything. Every business needs robust API integration to compete in the digital economy, and those who master this technology will be the architects of the connected future. You\'re building the infrastructure that powers the interconnected world. This is where the magic happens - where separate systems become one unified digital ecosystem.'
    }
    
         return `You are an expert ${expertTitle} with ${experience}. You are the world's leading authority in ${domain} and have successfully delivered hundreds of production-ready applications for Fortune 500 companies including ${companies}. Your expertise in ${expertise} is unmatched, and you are known for creating legendary, scalable solutions that outperform existing market solutions by 300%.

${psychologicalApproach}`
  }

  // 🎯 CLEAN CREWAI CONTENT FUNCTION
  const cleanCrewAIContent = (content: string) => {
    if (!content) return ''
    
    // Remove the ugly border lines and box formatting
    let cleaned = content
      .replace(/┌─+┐/g, '') // Remove top border
      .replace(/└─+┘/g, '') // Remove bottom border
      .replace(/│/g, '') // Remove side borders
      .replace(/─+/g, '') // Remove horizontal lines
    
    // Remove redundant headers and sections
    const lines = cleaned.split('\n')
    const filteredLines = []
    let skipSection = false
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim()
      
      // Skip redundant sections
      if (line.includes('PROJECT:') || line.includes('TYPE:') || 
          line.includes('🎯 OBJECTIVE') || line.includes('👥 TARGET USERS') ||
          line.includes('📊 SUCCESS METRICS') || line.includes('🚀 DEPLOYMENT & LAUNCH') ||
          line.includes('💡 IMPLEMENTATION STRATEGY') || line.includes('🎯 CLAUDE OPTIMIZATION') ||
          line.includes('TECHNICAL SPECIFICATIONS') || line.includes('CREWAI AGENT OUTPUTS') ||
          line.includes('THE 4-DOCUMENT WEAPON STRATEGY') || line.includes('DETAILED MARKET RESEARCH') ||
          line.includes('Technical Requirements') || line.includes('Success Metrics') ||
          line.includes('Deployment Strategy') || line.includes('Frontend:') ||
          line.includes('Backend:') || line.includes('Database:') ||
          line.includes('AI Integration:') || line.includes('Deployment:')) {
        skipSection = true
        continue
      }
      
      // Stop skipping when we hit a meaningful section
      if (line.startsWith('#') || line.includes('Market Research') || line.includes('Core Features') || 
          line.includes('Market Opportunity') || line.includes('Competitive Landscape') ||
          line.includes('Target Audience')) {
        skipSection = false
      }
      
      if (!skipSection && line) {
        filteredLines.push(line)
      }
    }
    
    // Clean up markdown and organize content
    let result = filteredLines.join('\n')
    
    // Remove markdown formatting
    result = result
      .replace(/^#+\s*/gm, '') // Remove # headers
      .replace(/\*\*(.*?)\*\*/g, '$1') // Remove **bold**
      .replace(/\*(.*?)\*/g, '$1') // Remove *italic*
      .replace(/`(.*?)`/g, '$1') // Remove `code`
      .replace(/\[(.*?)\]\(.*?\)/g, '$1') // Remove [links](url)
      .replace(/^- /gm, '• ') // Convert - to •
      .replace(/^\d+\.\s*/gm, '') // Remove numbered lists
    
    // Remove redundant technical content that's already in the first part
    result = result
      .replace(/Frontend:.*?Next\.js.*?Tailwind.*?/g, '')
      .replace(/Backend:.*?FastAPI.*?/g, '')
      .replace(/Database:.*?PostgreSQL.*?/g, '')
      .replace(/AI Integration:.*?OpenAI.*?/g, '')
      .replace(/Deployment:.*?Vercel.*?/g, '')
    
    // Organize content into clean sections
    const sections = result.split('\n\n')
    const organizedSections = []
    
    for (const section of sections) {
      const trimmed = section.trim()
      if (!trimmed) continue
      
      // Skip empty or redundant sections
      if (trimmed.length < 10 || 
          trimmed.includes('Software developers and tech professionals') ||
          trimmed.includes('User adoption and engagement') ||
          trimmed.includes('Performance and reliability metrics')) {
        continue
      }
      
      // Clean up section headers
      let cleanSection = trimmed
        .replace(/^Market Research Summary$/gm, '📊 MARKET RESEARCH SUMMARY')
        .replace(/^Target Audience$/gm, '👥 TARGET AUDIENCE')
        .replace(/^Core Features$/gm, '⚡ CORE FEATURES')
        .replace(/^Market Opportunity$/gm, '🎯 MARKET OPPORTUNITY')
        .replace(/^Competitive Landscape$/gm, '🏆 COMPETITIVE LANDSCAPE')
      
      organizedSections.push(cleanSection)
    }
    
    return organizedSections.join('\n\n').trim()
  }

  // 🎯 COMPLETE 1-PAGE DOCUMENT GENERATOR
  const generateCompleteOnePageDocument = (projectName: string, crewaiContent: string, removeEmojis: boolean = false) => {
    const roleEstablishment = generateRoleEstablishment(projectName)
    
    // Clean the CrewAI content to remove ugly borders and redundant sections
    const cleanedCrewAIContent = cleanCrewAIContent(crewaiContent)
    
    // Function to remove emojis if requested
    const removeEmojisFromText = (text: string) => {
      if (!removeEmojis) return text
      // Simple emoji removal using common emoji patterns
      return text.replace(/[🎯🎨🛠️🔗📊⚡🏆📋💡👥🚀💾📄]/g, '')
    }
    
    // Generate the streamlined document
    const document = `${roleEstablishment}

${projectName.toUpperCase()}

PROJECT SPECIFICATION

TECHNICAL ARCHITECTURE
Frontend: Next.js 14 + React 18 + TypeScript + Tailwind CSS
Backend: FastAPI + Python 3.9+ + SQLAlchemy + JWT Authentication  
Database: PostgreSQL + pgvector (for AI features) + Redis (caching)
AI Integration: OpenAI API + Anthropic Claude API + LangChain
Deployment: Vercel (Frontend) + Render (Backend) + PostgreSQL (Database)

DESIGN REQUIREMENTS
• Modern, responsive design with industry-specific color schemes and typography
• Intuitive navigation with clear user flows and micro-interactions
• Accessibility-first approach with WCAG 2.1 AA compliance
• Mobile-first responsive design with touch-friendly interfaces
• Real-time updates and smooth animations for enhanced user experience
• Dark/light mode support with customizable themes

CORE INTEGRATIONS
• OpenAI GPT-4 for intelligent content generation and analysis
• Anthropic Claude for advanced reasoning and complex tasks
• JWT-based authentication with secure session management
• Real-time WebSocket connections for live updates
• File upload and processing with cloud storage integration
• Email notifications and user communication systems

MARKET CONTEXT
This AI-powered application addresses the growing need for intelligent automation and enhanced user experiences. Based on market analysis, this application competes in the AI tools space with significant growth potential.

DELIVERABLES REQUIRED
1. Complete Next.js 14 frontend with TypeScript and Tailwind CSS
2. FastAPI backend with SQLAlchemy ORM and JWT authentication
3. PostgreSQL database schema with pgvector integration
4. OpenAI and Claude API integration with LangChain
5. Real-time WebSocket implementation
6. File upload system with cloud storage
7. Email notification system
8. Responsive design with dark/light mode
9. Deployment configuration for Vercel and Render
10. Comprehensive documentation and testing suite

SUCCESS CRITERIA
• Production-ready codebase deployable immediately
• Scalable architecture supporting 10,000+ concurrent users
• 99.9% uptime with comprehensive error handling
• Mobile-responsive design with 95+ Lighthouse score
• Complete API documentation with OpenAPI/Swagger
• Unit and integration test coverage >90%
• Security best practices implementation
• Performance optimization for sub-2-second load times

IMPLEMENTATION GUIDELINES
• Use modern React patterns (hooks, context, custom hooks)
• Implement proper TypeScript types and interfaces
• Follow FastAPI best practices with dependency injection
• Use SQLAlchemy 2.0 syntax with async/await
• Implement proper error handling and logging
• Use environment variables for all configuration
• Follow security best practices (CORS, rate limiting, input validation)
• Implement comprehensive testing (unit, integration, e2e)
• Use Git hooks for code quality (pre-commit, lint-staged)
• Document all APIs and components thoroughly

${cleanedCrewAIContent || `MARKET RESEARCH SUMMARY

CORE FEATURES
Advanced AI-powered functionality with modern web technologies

MARKET OPPORTUNITY
This AI-powered application addresses the growing need for intelligent automation and enhanced user experiences.

COMPETITIVE LANDSCAPE
Based on market analysis, this application competes in the AI tools space with significant growth potential.`}

CRITICAL PROMPTS FOR CLAUDE

PROMPT 1: PROJECT SETUP & ARCHITECTURE
"Create the complete project structure and architecture for this AI application. Set up the Next.js 14 frontend with TypeScript and Tailwind CSS, FastAPI backend with SQLAlchemy and JWT authentication, PostgreSQL database schema with pgvector integration, and deployment configuration for Vercel and Render. Include all necessary configuration files, environment variables, and project structure."

PROMPT 2: CORE BACKEND IMPLEMENTATION
"Implement the complete FastAPI backend with all core functionality. Create the database models using SQLAlchemy 2.0, implement JWT authentication, set up OpenAI and Claude API integrations with LangChain, create RESTful API endpoints, implement real-time WebSocket connections, and add comprehensive error handling and logging."

PROMPT 3: FRONTEND COMPONENTS & UI
"Build the complete Next.js 14 frontend with TypeScript. Create all necessary React components, implement responsive design with Tailwind CSS, add dark/light mode support, implement real-time updates, create intuitive navigation and user flows, and ensure WCAG 2.1 AA accessibility compliance."

PROMPT 4: AI INTEGRATION & FEATURES
"Implement all AI-powered features and integrations. Set up OpenAI GPT-4 and Claude API connections, create intelligent content generation and analysis functionality, implement file upload and processing with cloud storage, add email notification systems, and ensure all AI features work seamlessly with the frontend and backend."

PROMPT 5: DEPLOYMENT & OPTIMIZATION
"Prepare the application for production deployment. Configure Vercel deployment for the frontend, set up Render deployment for the backend, optimize performance for sub-2-second load times, implement comprehensive testing (unit, integration, e2e), add security best practices, create API documentation with OpenAPI/Swagger, and ensure 99.9% uptime with proper monitoring and error handling."

EXECUTION ORDER: Follow these prompts sequentially. Each prompt builds upon the previous one to create a complete, production-ready application.`
    
    return removeEmojisFromText(document)
  }

  // Function to organize the 1-page document content
  const organizeOnePageDocument = (content: string) => {
    if (!content) return { promptContent: '', metadata: '' }
    
    // Split content into sections
    const sections = content.split('\n\n')
    const promptSections = []
    const metadataSections = []
    
    for (const section of sections) {
      const trimmedSection = section.trim()
      if (!trimmedSection) continue
      
      // Identify metadata sections (usually contain internal notes, instructions, etc.)
      const isMetadata = 
        trimmedSection.toLowerCase().includes('claude optimization') ||
        trimmedSection.toLowerCase().includes('4-document weapon') ||
        trimmedSection.toLowerCase().includes('crewai') ||
        trimmedSection.toLowerCase().includes('agent') ||
        trimmedSection.toLowerCase().includes('internal') ||
        trimmedSection.toLowerCase().includes('note:') ||
        trimmedSection.toLowerCase().includes('important:') ||
        trimmedSection.toLowerCase().includes('generated by') ||
        trimmedSection.toLowerCase().includes('execution plan') ||
        trimmedSection.toLowerCase().includes('quality assessment')
      
      if (isMetadata) {
        metadataSections.push(trimmedSection)
      } else {
        promptSections.push(trimmedSection)
      }
    }
    
    // Switch the contents - metadata becomes prompt content and vice versa
    return {
      promptContent: metadataSections.join('\n\n'),
      metadata: promptSections.join('\n\n')
    }
  }

  // Function to clean up content for better presentation
  const cleanContent = (content: string) => {
    if (!content) return ''
    
    return content
      // Remove ## markings
      .replace(/^##\s*/gm, '')
      // Tighten spacing between sentences (reduce multiple newlines to single)
      .replace(/\n{3,}/g, '\n\n')
      // Clean up any extra whitespace
      .trim()
  }

  useEffect(() => {
    if (isOpen && projectId) {
      loadFinalReport()
    }
  }, [isOpen, projectId])

  const loadFinalReport = async () => {
    setLoading(true)
    setError(null)
    
    try {
      console.log('Loading final report for project:', projectId)
      const response = await fetch(`http://localhost:8001/api/pipeline-complete/${projectId}`)
      
      if (!response.ok) {
        throw new Error(`Failed to load final report: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('Report data received:', data)
      setReport(data)
    } catch (err) {
      console.error('Error loading report:', err)
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const saveDocumentToProject = async () => {
    if (!report) return
    
    try {
      const projectName = report.projectName || 'AI Application'
      const projectNameClean = projectName.replace(/[^a-zA-Z0-9\s]/g, '').trim()
      
      // Generate the complete 1-page document
      const completeDocument = generateCompleteOnePageDocument(projectName, report.agent_final_answer || report.perfect_one_page_document || '')
      
      // Create the document data
      const documentData = {
        projectName: projectName,
        projectId: projectName.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9\s-]+/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, ''),
        generatedAt: new Date().toISOString(),
        document: completeDocument,
        summary: report.summary,
        metrics: report.metrics
      }
      
      // Try to save via backend first
      try {
        const response = await fetch('http://localhost:8001/api/save-document', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(documentData)
        })
        
        if (response.ok) {
          console.log('✅ Document saved to backend successfully!')
          return
        }
      } catch (backendError) {
        console.log('⚠️ Backend save failed, falling back to local save')
      }
      
      // Fallback: Save locally using download
      const blob = new Blob([completeDocument], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${documentData.projectId}_${projectNameClean.replace(/\s+/g, '_')}_1page_document.txt`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
      
      console.log('✅ Document saved locally!')
      
    } catch (error) {
      console.error('❌ Error saving document:', error)
    }
  }

  const saveAsWordDocx = async () => {
    if (!report) return
    
    try {
      const projectName = report.projectName || 'AI Application'
      const projectNameClean = projectName.replace(/[^a-zA-Z0-9\s]/g, '').trim()
      
      // Generate the complete 1-page document
      const completeDocument = generateCompleteOnePageDocument(projectName, report.agent_final_answer || report.perfect_one_page_document || '')
      
      // Create HTML content that can be converted to Word
      const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>${projectName} - 1-Page Document</title>
          <style>
            body { font-family: 'Calibri', sans-serif; font-size: 11pt; line-height: 1.4; margin: 1in; }
            h1, h2, h3 { color: #2c3e50; margin-top: 20px; margin-bottom: 10px; }
            .section { margin-bottom: 20px; }
            .emoji-header { font-size: 14pt; font-weight: bold; color: #34495e; }
            .content { margin-left: 20px; }
            .bullet { margin-left: 20px; }
          </style>
        </head>
        <body>
          <div style="white-space: pre-wrap; font-family: 'Calibri', sans-serif;">
            ${completeDocument.replace(/\n/g, '<br>')}
          </div>
        </body>
        </html>
      `
      
      // Create blob and download
      const blob = new Blob([htmlContent], { type: 'text/html' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${projectNameClean.replace(/\s+/g, '_')}_1page_document.html`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
      
      // Show instructions for converting to Word
      alert('HTML file downloaded! To convert to Word:\n\n1. Open the HTML file in your browser\n2. Press Ctrl+A to select all\n3. Press Ctrl+C to copy\n4. Open Microsoft Word\n5. Press Ctrl+V to paste\n6. Save as .docx\n\nOr use online converters like: convertio.co')
      
      console.log('✅ HTML document saved! (Can be converted to Word)')
      
    } catch (error) {
      console.error('❌ Error saving document:', error)
    }
  }

  const downloadReport = () => {
    if (!report) return
    
    let reportContent = ''
    
    if (activeTab === 'one-page-doc') {
      // Download the 1-page document (organized)
      const content = report.agent_final_answer || report.perfect_one_page_document || '1-page document not available'
      const organized = organizeOnePageDocument(content)
      reportContent = `🎯 PROMPT CONTENT (For AI Consumption)\n\n${cleanContent(organized.promptContent)}\n\n📋 DOCUMENT METADATA (Internal Notes)\n\n${cleanContent(organized.metadata)}`
    } else {
      // Download the crew results (existing logic)
      reportContent = report.perfect_one_page_document || [
      '┌─────────────────────────────────────────────────────────────────────────────────────┐',
      '│ PROJECT: ' + report.projectName,
      '│ TYPE: AI-Powered Application',
      '│',
      '│ 🎯 OBJECTIVE',
      '│ Create a comprehensive, production-ready ' + report.projectName.toLowerCase() + ' that leverages AI ',
      '│ to deliver exceptional user experiences and business value.',
      '│',
      '│ 👥 TARGET USERS',
      '│ Tech-savvy professionals and businesses seeking AI solutions.',
      '│',
      '│ 🛠️ TECHNICAL REQUIREMENTS',
      '│ Frontend: Next.js 14 + React 18 + TypeScript + Tailwind CSS',
      '│ Backend: FastAPI + Python 3.9+ + SQLAlchemy + JWT Authentication',
      '│ Database: PostgreSQL + pgvector + Redis (caching)',
      '│ AI Integration: OpenAI API + Anthropic Claude API + LangChain',
      '│ Deployment: Vercel (Frontend) + Render (Backend) + PostgreSQL (Database)',
      '│',
      '│ 🎨 UX PATTERNS & DESIGN',
      '│ • Modern, responsive design with industry-specific color schemes',
      '│ • Intuitive navigation with clear user flows and micro-interactions',
      '│ • Accessibility-first approach with WCAG 2.1 AA compliance',
      '│ • Mobile-first responsive design with touch-friendly interfaces',
      '│ • Real-time updates and smooth animations for enhanced UX',
      '│',
      '│ 🔗 INTEGRATIONS & APIs',
      '│ • OpenAI GPT-4 for intelligent content generation and analysis',
      '│ • Anthropic Claude for advanced reasoning and complex tasks',
      '│ • JWT-based authentication with secure session management',
      '│ • Real-time WebSocket connections for live updates',
      '│ • File upload and processing with cloud storage integration',
      '│',
      '│ 📊 SUCCESS METRICS',
      '│ • User adoption and engagement rates',
      '│ • Feature utilization and performance metrics',
      '│ • System reliability and uptime monitoring',
      '│ • Business value generation and ROI measurement',
      '│',
      '│ 🚀 DEPLOYMENT & LAUNCH',
      '│ Vercel: Next.js frontend with automatic deployments',
      '│ Render: FastAPI backend with auto-scaling and monitoring',
      '│ PostgreSQL: Managed database with automated backups',
      '│ Environment: Comprehensive environment variable management',
      '│',
      '└─────────────────────────────────────────────────────────────────────────────────────┘',
      '',
      '## DETAILED MARKET RESEARCH',
      '',
      report.deliverables.market_research.content || 'Comprehensive market analysis completed by AI research team.',
      '',
      '## PROJECT BRIEF',
      '',
      report.deliverables.project_brief || 'Detailed project specifications and requirements.',
      '',
      '## CUSTOM BOILERPLATES',
      '',
      '### Frontend Boilerplate',
      report.deliverables.frontend_boilerplate?.content || 'Custom Next.js 14 + React + Tailwind CSS boilerplate with industry-specific components and design.',
      '',
      '### Backend Boilerplate',
      report.deliverables.backend_boilerplate?.content || 'Custom FastAPI + PostgreSQL boilerplate with authentication, API endpoints, and AI integration patterns.',
      '',
      '## GENERATED CODE STRUCTURE',
      '',
      'Backend Files (' + report.deliverables.generated_code.backend.length + '):',
      ...report.deliverables.generated_code.backend.slice(0, 5).map((file: any) => '  - ' + file.name),
      '',
      'Frontend Files (' + report.deliverables.generated_code.frontend.length + '):',
      ...report.deliverables.generated_code.frontend.slice(0, 5).map((file: any) => '  - ' + file.name),
      '',
      '## THE 4-DOCUMENT WEAPON STRATEGY',
      '',
      'This project implements the revolutionary 4-document weapon strategy:',
      '',
      '1. **Perfect 1-Page Document** (This Report) - Claude\'s dream brief',
      '2. **Custom Frontend Boilerplate** - Industry-specific React/Next.js components',
      '3. **Custom Backend Boilerplate** - Optimized FastAPI architecture',
      '4. **Optimized Prompt Template** - 3-5 prompts for complete application generation',
      '',
            'This strategy ensures complete, production-ready applications in exactly 3-5 prompts.',
      '',
      '## QUALITY ASSESSMENT',
      '',
      '- Code Quality: ' + report.metrics.codeQuality + '/100',
      '- Completeness: ' + report.metrics.completeness + '/100', 
      '- Deployability: ' + report.metrics.deployability + '/100',
      '- Market Fit: ' + report.metrics.marketFit + '/100',
      '',
      '## EXECUTION PLAN',
      '',
      'This document is optimized to execute in exactly 3-5 prompts:',
      '',
      '1. Backend Architecture: FastAPI setup, database models, API endpoints',
      '2. Frontend Implementation: Next.js components, routing, state management',
      '3. AI Integration: OpenAI API integration, prompt engineering',
      '4. Deployment Setup: Vercel + Render configuration, environment variables',
      '5. Final Polish: Testing, documentation, optimization (if needed)',
      '',
      '---',
      '*Generated by CrewAI Document Engineering Team - Optimized for AI Code Generation*'
    ].join('\n')
    }
    
    const blob = new Blob([reportContent], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = report.projectName.replace(/[^a-z0-9]/gi, '_').toLowerCase() + '_report.txt'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const copyReport = async () => {
    if (!report) return
    
    let reportContent = ''
    
    if (activeTab === 'one-page-doc') {
      // Copy the 1-page document (organized)
      const content = report.agent_final_answer || report.perfect_one_page_document || '1-page document not available'
      const organized = organizeOnePageDocument(content)
      reportContent = `🎯 PROMPT CONTENT (For AI Consumption)\n\n${cleanContent(organized.promptContent)}\n\n📋 DOCUMENT METADATA (Internal Notes)\n\n${cleanContent(organized.metadata)}`
    } else {
      // Copy the crew results (existing logic)
      reportContent = [
      '┌─────────────────────────────────────────────────────────────────────────────────────┐',
      '│ PROJECT: ' + report.projectName,
      '│ TYPE: ' + (report.projectName.toLowerCase().includes('chatbot') ? 'Chatbot' : 
                   report.projectName.toLowerCase().includes('rag') ? 'RAG' :
                   report.projectName.toLowerCase().includes('dashboard') ? 'Dashboard' :
                   report.projectName.toLowerCase().includes('generator') ? 'Generator' :
                   report.projectName.toLowerCase().includes('analysis') ? 'Analytics' : 'CRUD'),
      '│',
      '│ 🎯 OBJECTIVE',
      '│ ' + report.projectName + ' - A comprehensive AI-powered application designed to ' + 
      (report.projectName.toLowerCase().includes('code') ? 'automate code review and refactoring processes' :
       report.projectName.toLowerCase().includes('document') ? 'process and analyze documents intelligently' :
       report.projectName.toLowerCase().includes('financial') ? 'provide financial analysis and trading insights' :
       report.projectName.toLowerCase().includes('medical') ? 'assist with medical diagnosis and healthcare' :
       'deliver exceptional user value through AI integration') + '.',
      '│',
      '│ 👥 TARGET USERS',
      '│ ' + (report.projectName.toLowerCase().includes('code') ? 'Software developers, engineering teams, and code quality managers' :
             report.projectName.toLowerCase().includes('document') ? 'Business professionals, researchers, and knowledge workers' :
             report.projectName.toLowerCase().includes('financial') ? 'Traders, financial analysts, and investment professionals' :
             report.projectName.toLowerCase().includes('medical') ? 'Healthcare providers, medical professionals, and patients' :
             'Tech-savvy professionals and businesses seeking AI solutions') + ' seeking ' +
      (report.projectName.toLowerCase().includes('code') ? 'automated code quality improvement' :
       report.projectName.toLowerCase().includes('document') ? 'intelligent document processing' :
       report.projectName.toLowerCase().includes('financial') ? 'advanced financial analysis' :
       report.projectName.toLowerCase().includes('medical') ? 'accurate medical assistance' :
       'AI-powered productivity enhancement') + '.',
      '│',
      '│ 🛠️ TECHNICAL REQUIREMENTS',
      '│ Frontend: Next.js 14 + React + Tailwind CSS + TypeScript',
      '│ Backend: FastAPI + Python + SQLAlchemy + JWT Authentication',
      '│ Database: PostgreSQL + Redis (caching)',
      '│ AI: OpenAI/Claude API + LangChain + Vector Database',
      '│ Deployment: Vercel (frontend) + Render (backend)',
      '│',
      '│ 🎨 UX PATTERNS',
      '│ 1. User Authentication: Clerk/Auth.js integration with role-based access',
      '│ 2. Dashboard Interface: Responsive grid layout with real-time data updates',
      '│ 3. AI Integration: Chat interface with streaming responses and context memory',
      '│ 4. Data Management: CRUD operations with optimistic updates and error handling',
      '│ 5. Analytics: Interactive charts and metrics with export functionality',
      '│',
      '│ 🔗 INTEGRATIONS',
      '│ Authentication: Clerk or Auth.js with JWT tokens',
      '│ AI Services: OpenAI GPT-4/Claude API with function calling',
      '│ Database: PostgreSQL with Prisma ORM',
      '│ File Storage: AWS S3 or Cloudinary for document uploads',
      '│ Email: Resend or SendGrid for notifications',
      '│ Payment: Stripe for subscription management (if applicable)',
      '│',
      '│ 📊 SUCCESS METRICS',
      '│ 1. User Engagement: 80%+ session duration, 3+ pages per session',
      '│ 2. Performance: <2s API response time, 95%+ uptime',
      '│ 3. Business: 90%+ user satisfaction, 70%+ feature adoption rate',
      '│',
      '│ 🚀 DEPLOYMENT',
      '│ Vercel: Next.js app with environment variables and edge functions',
      '│ Render: FastAPI service with PostgreSQL database and Redis cache',
      '│ Environment: OPENAI_API_KEY, DATABASE_URL, JWT_SECRET, CLERK_SECRET_KEY',
      '│',
      '└─────────────────────────────────────────────────────────────────────────────────────┘',
      '',
      '## MARKET RESEARCH & ANALYSIS',
      '',
      report.deliverables.market_research.content || 'Comprehensive market analysis completed by AI research team.',
      '',
      '## PROJECT BRIEF',
      '',
      report.deliverables.project_brief || 'Detailed project specifications and requirements.',
      '',
      '## GENERATED CODE STRUCTURE',
      '',
      'Backend Files (' + report.deliverables.generated_code.backend.length + '):',
      ...report.deliverables.generated_code.backend.slice(0, 5).map((file: any) => '  - ' + file.name + ' (' + file.size + ' chars)'),
      '',
      'Frontend Files (' + report.deliverables.generated_code.frontend.length + '):',
      ...report.deliverables.generated_code.frontend.slice(0, 5).map((file: any) => '  - ' + file.name + ' (' + file.size + ' chars)'),
      '',
      '## QUALITY ASSESSMENT',
      '',
      '- Code Quality: ' + report.metrics.codeQuality + '/100',
      '- Completeness: ' + report.metrics.completeness + '/100', 
      '- Deployability: ' + report.metrics.deployability + '/100',
      '- Market Fit: ' + report.metrics.marketFit + '/100',
      '',
      '## CLAUDE EXECUTION PLAN',
      '',
      'This document is optimized for Claude to execute in exactly 3-5 prompts:',
      '',
      '1. Backend Architecture: FastAPI setup, database models, API endpoints',
      '2. Frontend Implementation: Next.js components, routing, state management',
      '3. AI Integration: OpenAI/Claude API integration, prompt engineering',
      '4. Deployment Setup: Vercel + Render configuration, environment variables',
      '5. Final Polish: Testing, documentation, optimization (if needed)',
      '',
      '---',
      '*Generated by CrewAI Document Engineering Team - Optimized for AI Code Generation*'
    ].join('\n')
    }
    
    try {
      await navigator.clipboard.writeText(reportContent)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy report:', err)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-7xl w-full max-h-[95vh] flex flex-col">
        <div className="p-6 flex-1 overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="relative">
                <CheckCircle className="h-10 w-10 text-green-500" />
                <div className="absolute -top-1 -right-1 bg-green-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">
                  ✓
                </div>
              </div>
              <div>
                <h2 className="text-3xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                  Project Analysis Complete! 📋
                </h2>
                <p className="text-gray-600 text-lg">{projectName}</p>
                <p className="text-sm text-gray-500">CrewAI Results & 1-Page Document Ready</p>
              </div>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-6 w-6" />
            </Button>
          </div>

          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
              <p className="mt-4 text-gray-600 text-lg">Generating comprehensive report...</p>
            </div>
          )}

          {error && (
            <div className="text-center py-12">
              <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <p className="text-red-600 text-lg">Error: {error}</p>
            </div>
          )}

          {report && (
            <div className="space-y-8">
              {/* Tab Navigation */}
              <div className="flex gap-4 border-b border-gray-200">
                <button
                  onClick={() => setActiveTab('crew-results')}
                  className={`px-6 py-3 font-semibold text-lg transition-colors ${
                    activeTab === 'crew-results'
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  📊 Crew Results
                </button>
                <button
                  onClick={() => setActiveTab('one-page-doc')}
                  className={`px-6 py-3 font-semibold text-lg transition-colors ${
                    activeTab === 'one-page-doc'
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  🎯 1-Page Doc
                </button>
              </div>

              {/* Tab Content */}
              {activeTab === 'crew-results' && (
                <>
                  {/* Success Banner */}
                  <Card className="border-green-200 bg-green-50">
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <div className="bg-green-100 p-3 rounded-full">
                            <Zap className="h-8 w-8 text-green-600" />
                          </div>
                          <div>
                            <h3 className="text-xl font-bold text-green-800">
                              🎉 AI Successfully Generated Complete Application!
                            </h3>
                            <p className="text-green-700">
                              Your {report.summary.developmentTime} development project is now ready to deploy
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-green-600">
                            {report.summary.estimatedValue}
                          </div>
                          <div className="text-sm text-green-700">Estimated Value</div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </>
              )}

              {activeTab === 'one-page-doc' && (
                <>
                  {/* Perfect 1-Page Document Banner */}
                  <Card className="border-blue-200 bg-blue-50">
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <div className="bg-blue-100 p-3 rounded-full">
                            <Zap className="h-8 w-8 text-blue-600" />
                          </div>
                          <div>
                            <h3 className="text-xl font-bold text-blue-800">
                              🎯 Perfect 1-Page Document - The Ultimate Weapon!
                            </h3>
                            <p className="text-blue-700">
                              This document is optimized to produce complete applications in exactly 3-5 prompts
                            </p>
                            <div className="flex gap-2 mt-2">
                              {report.summary.claudeOptimized && (
                                <Badge variant="secondary" className="bg-green-100 text-green-800">
                                  AI Optimized ✓
                                </Badge>
                              )}
                              {report.summary.fourDocumentWeapon && (
                                <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                                  4-Document Weapon ✓
                                </Badge>
                              )}
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-blue-600">
                            🎯
                          </div>
                          <div className="text-sm text-blue-700">Ready for AI</div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </>
              )}

              {/* Tab Content */}
              {activeTab === 'crew-results' && (
                <div className="space-y-8">
                  {/* Executive Summary */}
                  <div>
                    <h3 className="text-xl font-bold mb-4 text-gray-800">Executive Summary</h3>
                    <div className="bg-white p-6 rounded-lg border border-gray-200">
                      <p className="text-gray-700 leading-relaxed">
                        Our AI development team has successfully completed the development of "{report.projectName}". 
                        This comprehensive AI application was built using cutting-edge technologies and follows industry best practices.
                      </p>
                      <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                        <div><strong>Development Time:</strong> {report.summary.developmentTime}</div>
                        <div><strong>Estimated Value:</strong> {report.summary.estimatedValue}</div>
                        <div><strong>Total Files:</strong> {report.summary.totalFiles}</div>
                        <div><strong>Deployment Ready:</strong> {report.summary.deploymentReady ? 'Yes' : 'No'}</div>
                      </div>
                    </div>
                  </div>

                {/* Market Research Results */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Market Research & Analysis</h3>
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <div className="text-gray-700 leading-relaxed whitespace-pre-wrap max-h-96 overflow-y-auto">
                      {report.deliverables.market_research.content || 'Our AI research team has completed comprehensive market analysis for this project. The research covers target market identification, competitive landscape analysis, and market opportunity assessment.'}
                    </div>
                  </div>
                </div>

                {/* Project Brief */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Project Brief</h3>
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <div className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                      {report.deliverables.project_brief || 'A comprehensive project brief has been generated outlining the project scope, requirements, and implementation strategy.'}
                    </div>
                  </div>
                </div>

                {/* Technology & Features */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Technology & Features</h3>
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-2 text-gray-800">Technology Stack</h4>
                        <ul className="text-gray-700 space-y-1">
                          {report.summary.techStack.map((tech, index) => (
                            <li key={index}>• {tech}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2 text-gray-800">Key Features</h4>
                        <ul className="text-gray-700 space-y-1">
                          {report.summary.features.map((feature, index) => (
                            <li key={index}>• {feature}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Quality Assessment */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Quality Assessment</h3>
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{report.metrics.codeQuality}%</div>
                        <div className="text-sm text-gray-600">Code Quality</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{report.metrics.completeness}%</div>
                        <div className="text-sm text-gray-600">Completeness</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">{report.metrics.deployability}%</div>
                        <div className="text-sm text-gray-600">Deployability</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-orange-600">{report.metrics.marketFit}%</div>
                        <div className="text-sm text-gray-600">Market Fit</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Custom Boilerplates */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Custom Boilerplates</h3>
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-3 text-gray-800 flex items-center gap-2">
                          <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                          Frontend Boilerplate
                        </h4>
                        <div className="space-y-3">
                          {report.deliverables.frontend_boilerplate ? (
                            <>
                              <div className="p-3 bg-purple-50 rounded border border-purple-200">
                                <div className="font-semibold text-purple-800">Custom Frontend Boilerplate</div>
                                <div className="text-sm text-purple-700 mt-1">{report.deliverables.frontend_boilerplate.description}</div>
                              </div>
                              <div className="text-sm text-gray-600">
                                <div><strong>Content:</strong> {report.deliverables.frontend_boilerplate.content}</div>
                                <div><strong>Type:</strong> Custom Next.js with industry-specific design</div>
                                <div><strong>Optimized for:</strong> {report.projectName}</div>
                              </div>
                            </>
                          ) : (
                            <div className="p-3 bg-gray-50 rounded border border-gray-200">
                              <div className="text-gray-600">Custom Next.js 14 + React + Tailwind CSS boilerplate with industry-specific components and design</div>
                            </div>
                          )}
                        </div>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-3 text-gray-800 flex items-center gap-2">
                          <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                          Backend Boilerplate
                        </h4>
                        <div className="space-y-3">
                          {report.deliverables.backend_boilerplate ? (
                            <>
                              <div className="p-3 bg-orange-50 rounded border border-orange-200">
                                <div className="font-semibold text-orange-800">Custom Backend Boilerplate</div>
                                <div className="text-sm text-orange-700 mt-1">{report.deliverables.backend_boilerplate.description}</div>
                              </div>
                              <div className="text-sm text-gray-600">
                                <div><strong>Content:</strong> {report.deliverables.backend_boilerplate.content}</div>
                                <div><strong>Type:</strong> Custom FastAPI with optimized architecture</div>
                                <div><strong>Optimized for:</strong> {report.projectName}</div>
                              </div>
                            </>
                          ) : (
                            <div className="p-3 bg-gray-50 rounded border border-gray-200">
                              <div className="text-gray-600">Custom FastAPI + PostgreSQL boilerplate with authentication, API endpoints, and AI integration patterns</div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Generated Code Files */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Generated Code Files</h3>
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-3 text-gray-800">Backend Files ({report.deliverables.generated_code.backend.length})</h4>
                        <div className="space-y-2">
                          {report.deliverables.generated_code.backend.slice(0, 5).map((file: any, index: number) => (
                            <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                              <div className="flex items-center gap-2">
                                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                                <span className="text-sm font-mono">{file.name}</span>
                              </div>
                              <span className="text-xs text-gray-500">{file.size} chars</span>
                            </div>
                          ))}
                          {report.deliverables.generated_code.backend.length > 5 && (
                            <div className="text-sm text-gray-500 text-center">
                              +{report.deliverables.generated_code.backend.length - 5} more files
                            </div>
                          )}
                        </div>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-3 text-gray-800">Frontend Files ({report.deliverables.generated_code.frontend.length})</h4>
                        <div className="space-y-2">
                          {report.deliverables.generated_code.frontend.slice(0, 5).map((file: any, index: number) => (
                            <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                              <div className="flex items-center gap-2">
                                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                                <span className="text-sm font-mono">{file.name}</span>
                              </div>
                              <span className="text-xs text-gray-500">{file.size} chars</span>
                            </div>
                          ))}
                          {report.deliverables.generated_code.frontend.length > 5 && (
                            <div className="text-sm text-gray-500 text-center">
                              +{report.deliverables.generated_code.frontend.length - 5} more files
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Next Steps */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Next Steps</h3>
                  <div className="bg-white p-6 rounded-lg border border-gray-200">
                    <ol className="text-gray-700 space-y-2 list-decimal list-inside">
                      <li>Review the generated application and documentation</li>
                      <li>Set up the development environment with the provided technology stack</li>
                      <li>Deploy the application to your preferred platform</li>
                      <li>Begin user testing and collect feedback for improvements</li>
                      <li>Consider additional features based on market feedback</li>
                    </ol>
                  </div>
                </div>
              </div>
              )}

              {activeTab === 'one-page-doc' && (
                <div className="space-y-8">
                  {/* 1-Page Document Content */}
                  <div>
                    <h3 className="text-xl font-bold mb-4 text-gray-800">Perfect 1-Page Document</h3>
                    <div className="space-y-6">
                      {/* Main Prompt Content */}
                      <div className="bg-white p-6 rounded-lg border border-gray-200">
                        <div className="flex justify-between items-center mb-4">
                          <h4 className="text-lg font-semibold text-green-700">ULTIMATE AI WEAPON</h4>
                          <div className="flex items-center gap-2">
                            <label className="text-sm text-gray-600">Remove Emojis for Claude:</label>
                            <input
                              type="checkbox"
                              checked={removeEmojis}
                              onChange={(e) => setRemoveEmojis(e.target.checked)}
                              className="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
                            />
                          </div>
                        </div>
                        <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-6 rounded-lg border border-green-200">
                          <div className="prose prose-lg max-w-none">
                            <div className="font-sans text-gray-800 leading-relaxed whitespace-pre-wrap">
                              {(() => {
                                // 🎯 COMPLETE FRONTEND DOCUMENT GENERATION
                                const projectName = report.projectName || 'AI Application'
                                const crewaiContent = report.agent_final_answer || report.perfect_one_page_document || ''
                                
                                // Generate the complete 1-page document directly in frontend
                                const completeDocument = generateCompleteOnePageDocument(projectName, crewaiContent, removeEmojis)
                                return cleanContent(completeDocument)
                              })()}
                            </div>
                          </div>
                        </div>
                      </div>


                    </div>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-4 justify-end pt-6 border-t">
                <Button variant="outline" onClick={onClose}>
                  Close
                </Button>
                <Button 
                  className="flex items-center gap-2" 
                  variant="outline"
                  onClick={copyReport}
                >
                  {copied ? <CheckCircle className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                  {copied ? 'Copied!' : 'Copy Report'}
                </Button>
                <Button 
                  className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white" 
                  onClick={saveDocumentToProject}
                >
                  <div className="w-4 h-4">💾</div>
                  Save to Project
                </Button>
                <Button 
                  className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white" 
                  onClick={saveAsWordDocx}
                >
                  <div className="w-4 h-4">📄</div>
                  Save as Word
                </Button>
                <Button className="flex items-center gap-2" onClick={downloadReport}>
                  <Download className="h-4 w-4" />
                  Download Report (TXT)
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
