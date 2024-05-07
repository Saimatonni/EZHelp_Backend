from exceptions.status_error import CustomHTTPException, InternalServerError
from config.db import db
from fastapi import HTTPException
from models.faq import FAQ, QuestionAnswer,Testimonial

class FAQController:
    @staticmethod
    def post_faq(faq_data: FAQ):
        try:
            id = faq_data.id
            name = faq_data.name
            contact = faq_data.contact
            question = faq_data.question
            
            faq = {
                "id": id,
                "name": name,
                "contact": contact,
                "question": question
            }
            db.get_collection("faqs").insert_one(faq)
            
            return faq
        except Exception as e:
            raise InternalServerError("Failed to post FAQ: " + str(e))

    @staticmethod
    def post_question_answer(qa_data: QuestionAnswer):
        try:
            question = qa_data.question
            answer = qa_data.answer
            
            qa = {
                "question": question,
                "answer": answer
            }
            db.get_collection("question_answers").insert_one(qa)
            
            return qa
        except Exception as e:
            raise InternalServerError("Failed to post question-answer: " + str(e))
        
    @staticmethod
    def get_all_question_answers():
        try:
            question_answers = list(db.get_collection("question_answers").find({}))
            for qa in question_answers:
                qa["_id"] = str(qa["_id"])
            return question_answers
        except Exception as e:
            raise InternalServerError("Failed to fetch question-answer data from the database: " + str(e))
        
class TestimonialController:
    @staticmethod
    def post_testimonial(testimonial_data: Testimonial):
        try:
            id = testimonial_data.id
            name = testimonial_data.name
            rate = testimonial_data.rate
            details = testimonial_data.details

            testimonial_dict = {
                "id": id,
                "name": name,
                "rate": rate,
                "details": details
            }

            db.get_collection("testimonials").insert_one(testimonial_dict)

            return testimonial_data

        except Exception as e:
            raise InternalServerError("Failed to post testimonial: " + str(e))
        
    @staticmethod
    def get_testimonials():
        try:
            testimonials = list(db.get_collection("testimonials").find({}))
            for testimonial in testimonials:
                testimonial["_id"] = str(testimonial["_id"])
            return testimonials
        except Exception as e:
            raise InternalServerError("Failed to fetch testimonials: " + str(e))
