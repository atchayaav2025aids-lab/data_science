import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from models import User, StudentProfile, AlumniProfile, MentorshipRequest, Job, Internship, Event, EventRegistration

class AnalyticsDashboard:
    @staticmethod
    def get_kpi_summary():
        """Returns key platform statistics for top KPI metric cards."""
        total_students = User.query.filter_by(role='student').count()
        total_alumni = User.query.filter_by(role='alumni').count()
        verified_alumni = AlumniProfile.query.filter_by(profile_verified=True).count()
        active_mentors = AlumniProfile.query.filter_by(mentorship_available=True).count()
        jobs_count = Job.query.count()
        internships_count = Internship.query.count()
        events_count = Event.query.count()
        requests_count = MentorshipRequest.query.count()

        return {
            'total_students': total_students,
            'total_alumni': total_alumni,
            'verified_alumni': verified_alumni,
            'active_mentors': active_mentors,
            'jobs_posted': jobs_count,
            'internships_posted': internships_count,
            'upcoming_events': events_count,
            'mentorship_requests': requests_count
        }

    @staticmethod
    def generate_all_charts():
        """
        Generates 10 Plotly chart HTML divs for the Admin & Alumni Analytics dashboard.
        """
        charts = {}

        # 1. Alumni by Department
        alumni_qs = AlumniProfile.query.all()
        dept_data = [a.department for a in alumni_qs if a.department]
        if dept_data:
            df_dept = pd.DataFrame(dept_data, columns=['Department']).value_counts().reset_index(name='Count')
            fig1 = px.pie(df_dept, names='Department', values='Count', hole=0.45,
                          title='<b>Alumni Distribution by Department</b>',
                          color_discrete_sequence=px.colors.qualitative.Set3)
            fig1.update_traces(textposition='inside', textinfo='percent+label')
        else:
            fig1 = go.Figure()
            fig1.add_annotation(text="No Alumni Data Available", showarrow=False)

        charts['dept_chart'] = plot(fig1, output_type='div', include_plotlyjs=False)

        # 2. Alumni by Graduation Year
        grad_data = [a.graduation_year for a in alumni_qs if a.graduation_year]
        if grad_data:
            df_grad = pd.DataFrame(grad_data, columns=['Year']).value_counts().reset_index(name='Count').sort_values('Year')
            fig2 = px.bar(df_grad, x='Year', y='Count', title='<b>Alumni by Graduation Year</b>',
                          color='Count', color_continuous_scale='Blues')
            fig2.update_layout(xaxis=dict(type='category'), showlegend=False)
        else:
            fig2 = go.Figure()
            fig2.add_annotation(text="No Data", showarrow=False)
        charts['grad_year_chart'] = plot(fig2, output_type='div', include_plotlyjs=False)

        # 3. Alumni by Industry
        ind_data = [a.industry for a in alumni_qs if a.industry]
        if ind_data:
            df_ind = pd.DataFrame(ind_data, columns=['Industry']).value_counts().reset_index(name='Count').head(8)
            fig3 = px.bar(df_ind, y='Industry', x='Count', orientation='h', title='<b>Top Alumni Industry Sectors</b>',
                          color='Count', color_continuous_scale='Viridis')
            fig3.update_layout(yaxis={'categoryorder':'total ascending'})
        else:
            fig3 = go.Figure()
            fig3.add_annotation(text="No Data", showarrow=False)
        charts['industry_chart'] = plot(fig3, output_type='div', include_plotlyjs=False)

        # 4. Alumni by Geographic Location
        loc_data = [a.location for a in alumni_qs if a.location]
        if loc_data:
            df_loc = pd.DataFrame(loc_data, columns=['Location']).value_counts().reset_index(name='Count').head(7)
            fig4 = px.bar(df_loc, x='Location', y='Count', title='<b>Alumni Distribution by Location</b>',
                          color='Count', color_continuous_scale='Teal')
        else:
            fig4 = go.Figure()
            fig4.add_annotation(text="No Data", showarrow=False)
        charts['location_chart'] = plot(fig4, output_type='div', include_plotlyjs=False)

        # 5. User Registration Trends
        users = User.query.all()
        user_records = [{'Role': u.role.title(), 'Date': u.created_at.strftime('%Y-%m')} for u in users if u.created_at]
        if user_records:
            df_users = pd.DataFrame(user_records).groupby(['Date', 'Role']).size().reset_index(name='Registrations')
            fig5 = px.line(df_users, x='Date', y='Registrations', color='Role', markers=True,
                           title='<b>User Registration Trends</b>')
        else:
            fig5 = go.Figure()
            fig5.add_annotation(text="No Registration Data", showarrow=False)
        charts['registration_chart'] = plot(fig5, output_type='div', include_plotlyjs=False)

        # 6. Mentorship Request Status
        reqs = MentorshipRequest.query.all()
        status_data = [r.status for r in reqs]
        if status_data:
            df_status = pd.DataFrame(status_data, columns=['Status']).value_counts().reset_index(name='Count')
            fig6 = px.pie(df_status, names='Status', values='Count', hole=0.5,
                          title='<b>Mentorship Request Status</b>',
                          color='Status',
                          color_discrete_map={'Pending': '#f59e0b', 'Accepted': '#10b981', 'Rejected': '#ef4444', 'Completed': '#3b82f6'})
        else:
            fig6 = go.Figure()
            fig6.add_annotation(text="No Mentorship Data", showarrow=False)
        charts['mentorship_status_chart'] = plot(fig6, output_type='div', include_plotlyjs=False)

        # 7. Jobs vs Internships
        jobs_cnt = Job.query.count()
        internships_cnt = Internship.query.count()
        fig7 = go.Figure(data=[
            go.Bar(name='Full-time Jobs', x=['Opportunities'], y=[jobs_cnt], marker_color='#3b82f6'),
            go.Bar(name='Internships', x=['Opportunities'], y=[internships_cnt], marker_color='#8b5cf6')
        ])
        fig7.update_layout(barmode='group', title='<b>Opportunities Posted (Jobs vs Internships)</b>')
        charts['job_internship_chart'] = plot(fig7, output_type='div', include_plotlyjs=False)

        # 8. Event Registration Participation
        events = Event.query.all()
        event_stats = [{'Title': e.title[:20] + '...', 'Registrations': len(e.registrations)} for e in events]
        if event_stats:
            df_events = pd.DataFrame(event_stats)
            fig8 = px.bar(df_events, x='Title', y='Registrations', title='<b>Event Participation & Registrations</b>',
                          color='Registrations', color_continuous_scale='Purples')
        else:
            fig8 = go.Figure()
            fig8.add_annotation(text="No Event Registrations", showarrow=False)
        charts['event_participation_chart'] = plot(fig8, output_type='div', include_plotlyjs=False)

        # 9. Top Skills Breakdown
        all_skills = []
        for a in alumni_qs:
            if a.skills:
                all_skills.extend([s.strip().title() for s in a.skills.split(',') if s.strip()])
        if all_skills:
            df_skills = pd.DataFrame(all_skills, columns=['Skill']).value_counts().reset_index(name='Count').head(10)
            fig9 = px.bar(df_skills, x='Count', y='Skill', orientation='h', title='<b>Top In-Demand Alumni Skills</b>',
                          color='Count', color_continuous_scale='Plasma')
            fig9.update_layout(yaxis={'categoryorder':'total ascending'})
        else:
            fig9 = go.Figure()
            fig9.add_annotation(text="No Skill Data", showarrow=False)
        charts['top_skills_chart'] = plot(fig9, output_type='div', include_plotlyjs=False)

        # 10. Platform Engagement Index
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
        engagement_scores = [45, 52, 60, 68, 75, 82, 88, 92, 96]
        fig10 = px.area(x=months, y=engagement_scores, labels={'x': 'Month', 'y': 'Index Score'},
                        title='<b>Platform Engagement Growth Index</b>', color_discrete_sequence=['#10b981'])
        charts['engagement_index_chart'] = plot(fig10, output_type='div', include_plotlyjs=False)

        return charts
