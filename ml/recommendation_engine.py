import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ml.preprocessing import preprocess_text, extract_keywords

class RecommendationEngine:
    @staticmethod
    def recommend_mentors(student_profile, alumni_profiles, top_n=10):
        """
        Calculates similarity between a StudentProfile and a list of AlumniProfiles.
        Returns a list of dicts containing alumni_profile, match_score, match_category, and match_reasons.
        """
        if not alumni_profiles or not student_profile:
            return []

        # Extract student text corpus
        student_skills = student_profile.skills or ""
        student_interests = student_profile.interests or ""
        student_goal = student_profile.career_goal or ""
        student_dept = student_profile.department or ""
        student_industry = student_profile.preferred_industry or ""
        
        student_combined = f"{student_skills} {student_interests} {student_goal} {student_industry}"
        student_clean = preprocess_text(student_combined)

        student_skill_set = extract_keywords(student_skills)
        student_interest_set = extract_keywords(student_interests)

        recommendations = []

        # Prepare text vectors for TF-IDF
        alumni_corpus = []
        for alum in alumni_profiles:
            alum_skills = alum.skills or ""
            alum_interests = alum.interests or ""
            alum_title = alum.job_title or ""
            alum_bio = alum.bio or ""
            alum_industry = alum.industry or ""
            alum_combined = f"{alum_skills} {alum_interests} {alum_title} {alum_bio} {alum_industry}"
            alumni_corpus.append(preprocess_text(alum_combined))

        # TF-IDF Vectorization
        all_documents = [student_clean] + alumni_corpus
        vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
        
        try:
            tfidf_matrix = vectorizer.fit_transform(all_documents)
            student_vector = tfidf_matrix[0]
            alumni_vectors = tfidf_matrix[1:]
            cosine_sims = cosine_similarity(student_vector, alumni_vectors)[0]
        except Exception:
            cosine_sims = [0.5] * len(alumni_profiles)

        for idx, alum in enumerate(alumni_profiles):
            raw_tfidf_sim = float(cosine_sims[idx]) if idx < len(cosine_sims) else 0.0

            # Direct feature matching rules
            reasons = []

            # 1. Skill Match
            alum_skills_raw = alum.skills or ""
            alum_skill_set = extract_keywords(alum_skills_raw)
            common_skills = student_skill_set.intersection(alum_skill_set)
            skill_score = len(common_skills) / max(len(student_skill_set), 1) if student_skill_set else 0.0
            if common_skills:
                matching_skill_str = ", ".join([s.title() for s in list(common_skills)[:4]])
                reasons.append(f"Matching Skills: {matching_skill_str}")

            # 2. Department Match
            dept_score = 0.0
            if student_dept and alum.department and (student_dept.lower() in alum.department.lower() or alum.department.lower() in student_dept.lower()):
                dept_score = 1.0
                reasons.append(f"Same Department ({alum.department})")

            # 3. Industry / Career Goal Match
            industry_score = 0.0
            alum_industry = (alum.industry or "").lower()
            alum_title = (alum.job_title or "").lower()
            student_ind = (student_industry or "").lower()
            student_cg = (student_goal or "").lower()

            if student_ind and alum_industry and (student_ind in alum_industry or alum_industry in student_ind):
                industry_score += 0.5
                reasons.append(f"Matching Industry ({alum.industry})")
            
            if student_cg and (student_cg in alum_title or student_cg in alum_industry or alum_title in student_cg):
                industry_score += 0.5
                reasons.append(f"Aligned Career Goal ({alum.job_title})")

            # 4. Interest Match
            alum_interest_set = extract_keywords(alum.interests or "")
            common_interests = student_interest_set.intersection(alum_interest_set)
            interest_score = len(common_interests) / max(len(student_interest_set), 1) if student_interest_set else 0.0
            if common_interests:
                matching_int_str = ", ".join([i.title() for i in list(common_interests)[:3]])
                reasons.append(f"Shared Interests: {matching_int_str}")

            # Weighted final similarity score calculation
            # Weights: TF-IDF (40%), Skill match (30%), Dept match (15%), Industry/Goal match (15%)
            final_score = (raw_tfidf_sim * 0.40) + (skill_score * 0.30) + (dept_score * 0.15) + (min(industry_score, 1.0) * 0.15)
            
            # Scaled score out of 100 with realistic dynamic range (min 45%, max 98%)
            scaled_score = int(round(min(max(final_score * 100 + 40, 52), 98)))

            # Fallback default reason if text similarity was low
            if not reasons:
                reasons.append("Experienced industry professional available for guidance")
                if alum.graduation_year:
                    reasons.append(f"Batch of {alum.graduation_year}")

            # Classification Category
            if scaled_score >= 90:
                category = "Excellent Match"
                badge_color = "green"
            elif scaled_score >= 75:
                category = "Strong Match"
                badge_color = "blue"
            elif scaled_score >= 60:
                category = "Good Match"
                badge_color = "amber"
            else:
                category = "Moderate Match"
                badge_color = "indigo"

            recommendations.append({
                'alumni': alum,
                'match_score': scaled_score,
                'match_category': category,
                'badge_color': badge_color,
                'reasons': reasons
            })

        # Sort recommendations by highest match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)

        return recommendations[:top_n]


    @staticmethod
    def recommend_internships(student_profile, internships, top_n=10):
        """
        Calculates match score between StudentProfile and listed Internships/Jobs.
        """
        if not student_profile or not internships:
            return []

        student_skills = student_profile.skills or ""
        student_goal = student_profile.career_goal or ""
        student_ind = student_profile.preferred_industry or ""

        student_skill_set = extract_keywords(student_skills)
        student_clean = preprocess_text(f"{student_skills} {student_goal} {student_ind}")

        recommendations = []

        internship_corpus = [preprocess_text(f"{item.title} {item.skills_required} {item.description} {item.company}") for item in internships]

        if internship_corpus:
            try:
                vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
                all_docs = [student_clean] + internship_corpus
                tfidf_matrix = vectorizer.fit_transform(all_docs)
                cosine_sims = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])[0]
            except Exception:
                cosine_sims = [0.5] * len(internships)
        else:
            cosine_sims = []

        for idx, item in enumerate(internships):
            tfidf_sim = float(cosine_sims[idx]) if idx < len(cosine_sims) else 0.0

            item_skills = item.skills_required or ""
            item_skill_set = extract_keywords(item_skills)
            common = student_skill_set.intersection(item_skill_set)

            reasons = []
            if common:
                reasons.append(f"{len(common)} matching required skills ({', '.join(list(common)[:3])})")
            if student_goal and student_goal.lower() in item.title.lower():
                reasons.append(f"Title directly matches career goal ({student_goal})")
            if student_ind and student_ind.lower() in item.description.lower():
                reasons.append(f"Preferred industry domain ({student_ind})")

            final_score = int(round(min(max(tfidf_sim * 60 + (len(common) * 15) + 45, 55), 98)))

            if not reasons:
                reasons.append("Relevant opportunity in your discipline")

            recommendations.append({
                'item': item,
                'match_score': final_score,
                'reasons': reasons
            })

        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:top_n]
