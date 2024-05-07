from fastapi import APIRouter, HTTPException, Header, Request
from controllers.faq import FAQController,TestimonialController
from models.faq import FAQ, QuestionAnswer,Testimonial

faq_router = APIRouter()

@faq_router.post("/faqs")
async def post_faq(faq_data: FAQ):
    try:
        faq = FAQController.post_faq(faq_data)
        faq["_id"] = str(faq["_id"])
        return {"message": "FAQ posted successfully", "data": faq}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@faq_router.post("/question-answers")
async def post_question_answer(qa_data: QuestionAnswer):
    try:
        qa = FAQController.post_question_answer(qa_data)
        qa["_id"] = str(qa["_id"])
        return {"message": "Question-Answer posted successfully", "data": qa}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@faq_router.get("/question-answers")
async def get_all_question_answers():
    try:
        question_answers = FAQController.get_all_question_answers()
        for qa in question_answers:
            qa["_id"] = str(qa["_id"])
        return {"data": question_answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@faq_router.post("/testimonials")
async def post_testimonial(testimonial_data: Testimonial):
    try:
        data = TestimonialController.post_testimonial(testimonial_data)
        return data
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@faq_router.get("/testimonials")
async def get_testimonials():
    try:
        data = TestimonialController.get_testimonials()
        return data
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))