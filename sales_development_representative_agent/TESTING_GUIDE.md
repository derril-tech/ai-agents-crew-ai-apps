# 🧪 SDR Assistant Testing Guide

## 🚀 Quick Start Verification

### 1. Backend Health Check
- **URL**: http://localhost:8000/health
- **Expected**: `{"status":"healthy"}`
- **Status**: ✅ Backend is running

### 2. Frontend Access
- **URL**: http://localhost:3000
- **Expected**: SDR Assistant dashboard loads with navigation
- **Status**: ✅ Frontend should be running

### 3. API Documentation
- **URL**: http://localhost:8000/docs
- **Expected**: FastAPI interactive documentation
- **Status**: ✅ Available for API testing

## 📋 Comprehensive Testing Checklist

### 🏠 Dashboard (Main Page)
- [ ] **Page Loads**: Dashboard displays with lead management interface
- [ ] **Navigation**: Sidebar shows all sections (Dashboard, Leads, Emails, Analytics, AI Tools, Settings)
- [ ] **Search Functionality**: Search bar filters leads by name, company, or email
- [ ] **Add Lead Button**: Opens form modal for single lead entry
- [ ] **Import CSV Button**: Allows CSV file upload for bulk lead import
- [ ] **Lead Cards**: Display lead information with action buttons
- [ ] **View Button**: Opens detailed lead modal
- [ ] **Edit Button**: Opens edit form with current data
- [ ] **Delete Button**: Removes lead with confirmation
- [ ] **Analyze Button**: Runs AI analysis on individual leads
- **Status**: ✅ All functionality implemented

### 👥 Leads Management
- [ ] **Single Lead Addition**:
  - Click "Add Lead" button
  - Fill form with test data:
    - Name: John Smith
    - Job Title: VP Engineering
    - Company: TechCorp Inc
    - Email: john.smith@techcorp.com
    - LinkedIn: https://linkedin.com/in/johnsmith
    - Company Website: https://techcorp.com
    - Use Case: AI implementation
  - Click "Add Lead"
  - Verify lead appears in the grid

- [ ] **Bulk CSV Import**:
  - Click "Import CSV" button
  - Upload `test_leads.csv` file
  - Verify all leads are imported
  - Check data accuracy

- [ ] **Lead Analysis**:
  - Select a lead and click "Analyze"
  - Wait for AI processing (30-60 seconds)
  - Verify analysis results include:
    - Lead score (0-100)
    - Priority level (High/Medium/Low)
    - Analysis details
    - Email draft generation

### ✉️ Email Management
- [ ] **Page Access**: Navigate to /emails
- [ ] **Email List**: View generated emails
- [ ] **Email Details**: Click view to see full email content
- [ ] **Email Actions**: Copy, edit, delete, send
- [ ] **Search & Filter**: Filter by status (draft, sent, scheduled)
- [ ] **Export**: Download email data as CSV
- **Status**: ✅ Mock data and UI implemented

### 📊 Analytics Dashboard
- [ ] **Page Access**: Navigate to /analytics
- [ ] **Overview Cards**: Total leads, conversion rate, response time, revenue
- [ ] **Monthly Trends**: Chart showing lead and revenue trends
- [ ] **Lead Sources**: Breakdown by source (LinkedIn, Website, etc.)
- [ ] **Top Performers**: Table of best performing SDRs
- [ ] **Time Range Filter**: Select different time periods
- [ ] **Export Function**: Download analytics data
- **Status**: ✅ Mock data and visualizations implemented

### 🤖 AI Tools
- [ ] **Page Access**: Navigate to /ai-tools
- [ ] **Tool Selection**: Choose from 6 AI tools:
  - Email Generator
  - Lead Scorer
  - Conversation Analyzer
  - Market Researcher
  - Pitch Optimizer
  - Lead Enrichment
- [ ] **Content Generation**: Click "Generate with AI" for each tool
- [ ] **Output Display**: View generated content
- [ ] **Copy/Download**: Copy to clipboard or download as file
- **Status**: ✅ Mock AI generation implemented

### ⚙️ Settings
- [ ] **Page Access**: Navigate to /settings
- [ ] **Profile Settings**: Update name, email, role, timezone
- [ ] **Notification Settings**: Toggle various notification types
- [ ] **AI Settings**: Configure AI model and features
- [ ] **Integrations**: Set up CRM, email, calendar connections
- [ ] **Security Settings**: Configure 2FA, session timeout, data retention
- [ ] **Save Changes**: Verify settings are saved
- **Status**: ✅ All settings categories implemented

## 🔗 API Integration Testing

### Backend API Endpoints
- [ ] **GET /health**: Health check
- [ ] **GET /leads**: Retrieve all leads
- [ ] **POST /leads**: Create new lead
- [ ] **PUT /leads/{id}**: Update lead
- [ ] **DELETE /leads/{id}**: Delete lead
- [ ] **POST /leads/analyze-bulk**: Analyze multiple leads
- [ ] **GET /emails**: Retrieve emails
- [ ] **POST /emails**: Create email
- [ ] **POST /emails/generate**: Generate AI email
- [ ] **GET /analytics**: Get analytics data
- [ ] **GET /dashboard**: Get dashboard data

### Frontend-Backend Communication
- [ ] **Server Status**: Check if backend connectivity indicator shows "Connected"
- [ ] **Data Loading**: Verify leads load from backend API
- [ ] **Real-time Updates**: Changes reflect immediately
- [ ] **Error Handling**: Graceful handling of API errors

## 🎯 Test Scenarios

### Scenario 1: Complete Lead Workflow
1. Add a new lead via form
2. Analyze the lead using AI
3. Generate personalized email
4. View email in email management
5. Export lead data

### Scenario 2: Bulk Operations
1. Import CSV with multiple leads
2. Run bulk analysis
3. Review all generated emails
4. Export results

### Scenario 3: Analytics Review
1. Navigate to analytics
2. Change time range filters
3. Review performance metrics
4. Export analytics data

## 🐛 Common Issues & Solutions

### Frontend Issues
- **No CSS Styling**: Ensure Tailwind CSS is properly configured
- **API Connection Errors**: Check backend is running on port 8000
- **Page Not Found**: Verify all page.tsx files exist in app directories

### Backend Issues
- **Import Errors**: Ensure all dependencies are installed with `uv sync`
- **API Errors**: Check environment variables and API keys
- **CORS Issues**: Verify CORS configuration in app.py

## ✅ Success Criteria

The application is fully functional when:
- [ ] All pages load without errors
- [ ] Navigation works between all sections
- [ ] CRUD operations work for leads
- [ ] AI analysis generates meaningful results
- [ ] Email generation produces personalized content
- [ ] Analytics display mock data correctly
- [ ] Settings can be modified and saved
- [ ] Export functionality works
- [ ] Search and filter features work
- [ ] Responsive design works on different screen sizes

## 🎉 Ready for Production

Once all tests pass, the SDR Assistant is ready for:
- User acceptance testing
- Data migration from existing systems
- Integration with real CRM systems
- Deployment to production environment

---

**Last Updated**: January 2025
**Version**: 1.0.0
**Status**: ✅ Ready for Testing
