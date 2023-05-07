from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Text, select
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from myclass.problem import ProblemData
import json
from myclass.problem import UserSubmitProblem, UserSubmitSolution
from datetime import datetime
from fastapi import HTTPException
from utils.utils import parse_problem_space_limit, parse_problem_time_limit

Base = declarative_base() # ORM 매핑을 위한 기본 클래스 

# 문제 테이블
class Problem(Base):
    __tablename__ = "problem"
    __table_args__ = {"schema" : "algopat"}

    problem_id = Column(BigInteger, primary_key=True, nullable=False)
    problem_title = Column(Text)
    problem_level = Column(BigInteger)
    problem_desc = Column(Text)
    problem_input = Column(Text)
    problem_output = Column(Text)
    problem_tag = Column(Text)
    problem_limit = Column(Text)
    problem_time_limit = Column(BigInteger)
    problem_space_limit = Column(BigInteger)


async def insert_problem(data : ProblemData, session): 
    # Problem 객체 생성
    problem = Problem(
        problem_id = data.problemId,
        problem_title = data.title,
        problem_level = data.level,
        problem_desc = data.problem_description,
        problem_input = data.problem_input,
        problem_output = data.problem_output,
        problem_tag = json.dumps(data.problem_tags, ensure_ascii = False),
        problem_limit = json.dumps(data.problem_limit, ensure_ascii=False),
        problem_time_limit = parse_problem_time_limit(data.problem_info_time_limit),
        problem_space_limit = parse_problem_space_limit(data.problem_info_space_limit)
    )

    # DB에 Problem 객체 추가
    async with session.begin():
        session.add(problem)
    await session.commit()
    await session.refresh(problem)
    await session.close()

async def check_problem_is_exist(problem_id : int, session):
    
    result = await session.execute(select(Problem).filter(Problem.problem_id == problem_id))
    problem = result.scalar()

    if problem is None:
        await session.close()
        return False # 문제 정보 없음
    else:
        await session.close()
        return True # 문제 정보 있음

# =================================================================================

# 문제 메타 데이터 테이블
class ProblemMeta(Base):
    __tablename__ = "problem_meta"
    __table_args__ = {"schema" : "algopat"}

    problem_id = Column(BigInteger, primary_key=True, nullable=False)
    problem_title = Column(Text)
    problem_submitted_count = Column(BigInteger)
    problem_master_user_seq = Column(Text) 

async def update_problem_meta(problem_id : int, user_seq : str, data : ProblemData, session):
    # 문제 메타 데이터 조회
    problem_meta = await session.get(ProblemMeta, problem_id)

    if problem_meta is not None:
        print("문제 메타 데이터 있음")
        # 문제 메타 데이터 업데이트 
        problem_meta.problem_submitted_count += 1
        problem_meta.problem_master_user_seq = user_seq # Todo : master user_seq logic
        await session.commit()
        await session.refresh(problem_meta)
        await session.close()
    else:
        print("문제 메타 데이터 없음")
        # 문제 메타 데이터 없음, 새로운 메타 데이터 추가 
        problem_meta = ProblemMeta(
            problem_id = problem_id,
            problem_title = data.title,
            problem_submitted_count = 1,
            problem_master_user_seq = user_seq # Todo : master user_seq logic 
        )

        session.add(problem_meta)
        await session.commit()
        await session.refresh(problem_meta)
        await session.close()

# =================================================================================

# 회원 푼 문제 테이블 
class UserSubmitProblem(Base):
    __tablename__ = "user_submit_problem"
    __table_args__ = {"schema" : "algopat"}

    problem_id = Column(BigInteger, primary_key=True)
    user_seq = Column(Text)
    user_submit_problem_created_at = Column(DateTime)
    user_submit_problem_updated_at = Column(DateTime)


async def insert_user_submit_problem(data : UserSubmitProblem, user_seq : str, session):
    user_submit_problem = UserSubmitProblem(
        problem_id = data.problem_id,
        user_seq = user_seq,
        user_submit_problem_created_at = datetime.now(),
        user_submit_problem_updated_at = datetime.now() # Todo : data.submissionTime 저장 logic 
    )

    # DB에 Problem 객체 추가
    async with session.begin():
        session.add(user_submit_problem)
    await session.commit()
    await session.refresh(user_submit_problem)
    await session.close()

    return user_submit_problem

async def get_user_submit_problem(problem_id : int, user_seq : str,  session):
    result = await session.execute(select(UserSubmitProblem).filter(UserSubmitProblem.problem_id == problem_id).filter(UserSubmitProblem.user_seq == user_seq))
    await session.close()
    return result.scalar()

#===============================================================================

# 회원 제출 코드 테이블
class UserSubmitSolution(Base):
    __tablename__ = "user_submit_solution"
    __table_args__ = {"schema" : "algopat"}

    submission_id = Column(BigInteger, primary_key=True)
    problem_id = Column(BigInteger)
    user_seq = Column(Text)
    user_submit_solution_time = Column(DateTime)
    user_submit_solution_result = Column(Text)
    user_submit_solution_result_category = Column(Text)
    user_submit_solution_language = Column(Text)
    user_submit_solution_code = Column(Text)
    user_submit_solution_runtime = Column(BigInteger)
    user_submit_solution_memory = Column(BigInteger)
    

async def insert_user_submit_solution(data : UserSubmitSolution, user_seq : str, session):
    user_submit_solution = UserSubmitSolution( 
        submission_id = data.submission_id,
        problem_id = data.problem_id,
        user_seq = user_seq,
        user_submit_solution_time = data.user_submit_solution_time,
        user_submit_solution_result = data.user_submit_solution_result,
        user_submit_solution_result_category = data.user_submit_solution_result_category, 
        user_submit_solution_language = data.user_submit_solution_language,
        user_submit_solution_code = data.user_submit_solution_code,
        user_submit_solution_runtime = data.user_submit_solution_runtime,
        user_submit_solution_memory = data.user_submit_solution_memory
    )

    # DB에 Problem 객체 추가
    async with session.begin():
        session.add(user_submit_solution)
    await session.commit()
    await session.refresh(user_submit_solution)
    await session.close()

    return user_submit_solution.submission_id

async def check_user_submit_solution_is_exist(submission_id : int, session):
    result = await session.execute(select(UserSubmitSolution).filter(UserSubmitSolution.submission_id == submission_id))
    user_submit_solution = result.scalar()

    if user_submit_solution is None:
        await session.close()
        return False # 회원제출코드 정보 없음
    else:
        await session.close()
        return True # 회원제출코드 정보 있음



#=================================================================================

# GPT 문제 요약 테이블 
class GPTProblemSummary(Base):
    __tablename__ = "gpt_problem_summary"
    __table_args__ = {"schema" : "algopat"}

    gpt_problem_summary_seq = Column(BigInteger, primary_key=True, autoincrement=True)
    problem_id = Column(BigInteger)
    gpt_problem_summary_description = Column(Text)
    gpt_problem_summary_input = Column(Text)
    gpt_problem_summary_output = Column(Text)
    gpt_problem_summary_constraints = Column(Text)
    gpt_time_complexity = Column(Text)
    gpt_time_complexity_reason = Column(Text)
    gpt_space_complexity = Column(Text)
    gpt_space_complexity_reason = Column(Text)
    problem_algorithm_type = Column(Text)
    problem_time_limit = Column(BigInteger)
    problem_space_limit = Column(BigInteger)


async def insert_gpt_problem_summary(data, session):
    gpt_problem_summary = GPTProblemSummary(
        problem_id = data.problem_id,
        gpt_problem_summary_description = data.gpt_problem_summary_description,
        gpt_problem_summary_input = data.gpt_problem_summary_input,
        gpt_problem_summary_output = data.gpt_problem_summary_output,
        gpt_problem_summary_constraints = data.gpt_problem_summary_constraints,
        gpt_time_complexity = data.gpt_time_complexity,
        gpt_time_complexity_reason = data.gpt_time_complexity_reason,
        gpt_space_complexity = data.gpt_space_complexity,
        gpt_space_complexity_reason = data.gpt_space_complexity_reason,
        problem_algorithm_type = data.problem_algorithm_type,
        problem_time_limit = parse_problem_time_limit(data.problem_time_limit),
        problem_space_limit = parse_problem_space_limit(data.problem_space_limit)
    )

    # DB에 Problem 객체 추가
    async with session.begin():
        session.add(gpt_problem_summary)
    await session.commit()
    await session.refresh(gpt_problem_summary)
    await session.close()

async def check_gpt_problem_summary_is_exist(problem_id : int, session):
    
    result = await session.execute(select(GPTProblemSummary).filter(GPTProblemSummary.problem_id == problem_id))
    problem = result.scalar()

    if problem is None:
        await session.close()
        return False # 문제 요약 정보 없음
    else:
        await session.close()
        return True # 문제 요약 정보 존재
        
async def get_gpt_problem_summary(problem_id : int, session):
    
    result = await session.execute(select(GPTProblemSummary).filter(GPTProblemSummary.problem_id == problem_id))
    await session.close()
    return result.scalar()
    
#==================================================================================================================

# GPT 평가 테이블 
class GPTSolution(Base):
    __tablename__ = "gpt_solution"
    __table_args__ = {"schema" : "algopat"}

    gpt_solution_seq = Column(BigInteger, primary_key=True, autoincrement=True)
    submission_id = Column(BigInteger)
    user_seq = Column(BigInteger)
    gpt_solution_time_complexity = Column(Text)
    gpt_solution_time_complexity_reason = Column(Text)
    gpt_solution_time_score = Column(BigInteger)
    gpt_solution_time_complexity_good_point = Column(Text)
    gpt_solution_time_complexity_bad_point = Column(Text)
    gpt_improving_time_complexity_suggestion = Column(Text)
    gpt_solution_space_complexity = Column(Text)
    gpt_solution_space_complexity_reason = Column(Text)
    gpt_solution_space_score = Column(BigInteger)
    gpt_solution_space_complexity_good_point = Column(Text)
    gpt_solution_space_complexity_bad_point = Column(Text)
    gpt_improving_space_complexity_suggestion = Column(Text)
    gpt_solution_clean_score = Column(BigInteger)
    gpt_solution_refactoring_suggestion = Column(Text)
    gpt_total_score = Column(BigInteger)

async def insert_gpt_solution(data : GPTSolution, user_seq : str, session):
    gpt_solution = GPTSolution(
        submission_id = data.submission_id,
        user_seq = user_seq,
        gpt_solution_time_complexity = data.gpt_solution_time_complexity,
        gpt_solution_time_complexity_reason = data.gpt_solution_time_complexity_reason,
        gpt_solution_time_score = data.gpt_solution_time_score,
        gpt_solution_time_complexity_good_point = data.gpt_solution_time_complexity_good_point,
        gpt_solution_time_complexity_bad_point = data.gpt_solution_time_complexity_bad_point,
        gpt_improving_time_complexity_suggestion = data.gpt_improving_time_complexity_suggestion,
        gpt_solution_space_complexity = data.gpt_solution_space_complexity,
        gpt_solution_space_complexity_reason = data.gpt_solution_space_complexity_reason,
        gpt_solution_space_score = data.gpt_solution_space_score,
        gpt_solution_space_complexity_good_point = data.gpt_solution_space_complexity_good_point,
        gpt_solution_space_complexity_bad_point = data.gpt_solution_space_complexity_bad_point,
        gpt_improving_space_complexity_suggestion = data.gpt_improving_space_complexity_suggestion,
        gpt_solution_clean_score = data.gpt_solution_clean_score,
        gpt_solution_refactoring_suggestion = data.gpt_solution_refactoring_suggestion,
        gpt_total_score = data.gpt_total_score
    )

    # DB에 Problem 객체 추가
    async with session.begin():
        session.add(gpt_solution)
    await session.commit()
    await session.refresh(gpt_solution)
    await session.close()

