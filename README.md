# 🤖 Rynova AI Client Dashboard

A modern, AI-themed Streamlit dashboard for managing AI Agent appointment clients and onboarding new businesses. Built for Rynova AI to streamline client management and track business integrations.

## ✨ Features

### 📊 Dashboard Overview
- **Real-time metrics** and KPIs for client portfolio
- **Interactive charts** with AI-themed dark design
- **Business type distribution** analysis
- **Integration status** monitoring and insights

### ➕ Smart Client Onboarding
- **Comprehensive form** with all business data fields
- **Smart CRM/Calendar logic**: SquareUp CRM auto-sets SquareUp Calendar
- **Validation system** with contextual error messages
- **Integration setup** for CRM, Calendar, and Communication tools
- **AI Agent configuration** and message templates

### 👥 Advanced Client Management
- **Search and filter** by business type, status, and more
- **Complete edit functionality** for all client fields
- **Client ID display** for easy reference
- **Real-time updates** to Supabase database
- **Bulk operations** and status management

### 📈 Business Analytics & Insights
- **Client activation rates** and conversion metrics
- **Integration adoption** tracking
- **Business type trends** and market analysis
- **Subscription analytics** and revenue insights
- **Performance dashboards** with visual KPIs

## 🎨 Modern Design

- **AI-themed dark UI** with glassmorphism effects
- **Gradient backgrounds** and smooth animations
- **Responsive design** that works on all screen sizes
- **Professional color palette** optimized for AI companies
- **Interactive elements** with hover effects and transitions

## 🚀 Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/Zavian3/rynova-ai.git
cd rynova-ai
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**:
```bash
streamlit run app.py
```

4. **Access the dashboard** at `http://localhost:8501`

## 🔧 Configuration

### Supabase Integration
The dashboard connects to Supabase for data storage and management:

- **Database**: Supabase PostgreSQL
- **Authentication**: API Key-based
- **Real-time updates**: Automatic synchronization

### API Endpoints
- `GET /rest/v1/client?select=*` - Fetch all clients
- `POST /rest/v1/client` - Create new client
- `PATCH /rest/v1/client?client_id=eq.{id}` - Update client
- `DELETE /rest/v1/client?client_id=eq.{id}` - Delete client

## 📋 Data Schema

### Client Information Structure

#### 🏢 Basic Information
- `client_id` - Unique identifier
- `business_name` - Business name
- `business_type` - salon, spa, clinic, dental, medical, fitness, restaurant, retail, consulting, other
- `phone` - Contact phone number
- `email` - Contact email address
- `street_address`, `city`, `state`, `zip_code`, `country` - Location data

#### 🔗 Integration Settings
- `crm_type` - Currently supports "squareup" only
- `crm_api_key` - SquareUp API key (required when CRM is selected)
- `calendar_type` - "squareup" (auto-set) or "google"
- `calendar_id` - Stores Calendar API key
- `twilio_number` - SMS communication number
- `front_desk_number` - Main business contact
- `front_desk_email` - Business email
- `google_review_link` - Review page URL

#### ⚙️ Business Settings
- `status` - active, pending, inactive, trial
- `subscription_plan` - basic, professional, enterprise, custom
- `subscription_expires_at` - Subscription end date
- `business_hours` - Operating schedule (JSON format)
- `features` - Enabled features array

#### 🤖 AI Agent Configuration
- `reminder_offsets` - Notification timing (JSON array)
- `follow_up_rules` - Automation rules (JSON)
- `rating_template` - Review request template
- `rating_high_template` - High rating follow-up
- `rating_low_template` - Low rating response
- `rating_offset_minutes` - Delay before rating request
- `promo_schedule` - Promotional campaign timing
- `reengage_rules` - Client re-engagement logic

## 🔄 Integration Logic

### CRM & Calendar Smart Logic
```
If CRM = SquareUp:
  ├── Calendar = SquareUp (automatic)
  ├── Requires: SquareUp API Key
  └── Requires: SquareUp Calendar API Key

If CRM = None:
  ├── Calendar = Google (optional)
  └── If Google: Requires Google Calendar API Key
```

## 📱 Dashboard Pages

1. **📊 Dashboard Overview** - Key metrics and recent activity
2. **➕ Add New Client** - Comprehensive onboarding form
3. **👥 Client Management** - Search, edit, and manage clients
4. **📈 Analytics** - Business insights and performance metrics

## 🛡️ Security Features

- **HTTPS encryption** for all API communications
- **Secure API key handling** through Supabase
- **Input validation** and sanitization
- **Error handling** with user-friendly messages
- **Data privacy** with proper access controls

## 🎯 Use Cases

- **Client Onboarding**: Streamline new business setup
- **Portfolio Management**: Track all clients in one place
- **Integration Monitoring**: Ensure all systems are connected
- **Business Analytics**: Make data-driven decisions
- **Status Tracking**: Monitor client lifecycle stages

## 🔧 Technical Stack

- **Frontend**: Streamlit with custom CSS
- **Database**: Supabase (PostgreSQL)
- **Charts**: Plotly with AI-themed styling
- **API**: RESTful API with Supabase
- **Styling**: Custom CSS with glassmorphism effects

## 📊 Analytics Features

- **Real-time KPIs**: Client counts, activation rates, integration status
- **Visual Charts**: Pie charts, bar charts, trend analysis
- **Business Intelligence**: Type distribution, subscription tracking
- **Performance Metrics**: Setup completion rates, client health scores

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For technical support, feature requests, or questions about Rynova AI:

- **Repository**: [https://github.com/Zavian3/rynova-ai](https://github.com/Zavian3/rynova-ai)
- **Issues**: Use GitHub Issues for bug reports and feature requests

## 📝 License

This project is developed for Rynova AI client management purposes.

---

**Built with ❤️ for AI-powered appointment management**
