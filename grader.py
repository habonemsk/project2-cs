
from abc import ABC, abstractmethod
from base_types import *
import execution
import time

class Grader(ABC):
    """
    Abstract base class for graders.
    """
    @classmethod
    @property
    @abstractmethod
    def identifier(self) -> str:
        """
        A human-readable identifier for the grader.
        """
        pass
        
    @classmethod
    def resolve_graders(cls, grader_names: List[str]) -> List['Grader']:
        subclass_mapping = {subclass.identifier: subclass for subclass in cls.__subclasses__()}
        instances = []
        for grader_name in grader_names:
            subclass = subclass_mapping.get(grader_name, CorrectnessGrader)
            instances.append(subclass())
        return instances
    
    @classmethod
    def run_function(cls, code: str, function_prototype: FunctionPrototype, test_case: TestCase) -> str:
        """
        Runs generated Python code against a given test case.
        """
        parameters = function_prototype.get_ordered_parameter_values(test_case)
        return execution.execute_function(code, parameters)
        pass
    
    @abstractmethod
    def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
        """
        Grades the provided solutions against the problem definitions.
        """
        pass
        
    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
        
class CorrectnessGrader(Grader):
    @classmethod
    @property
    def identifier(self):
        return "correctness"
        
    def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
        solutionGrades = []
        for problem in problems:
            function_prototype = problem.function_prototype
            for solution in solutions:
                number_correct = 0
                total_tests = 0
                issues = []
                if solution.problem_identifier == problem.identifier:
                    for test_case in problem.correctness_test_suite:
                        actual_result = Grader.run_function(solution.solution_code, function_prototype, test_case)
                        expected_result = function_prototype.get_return_values(test_case)
                        total_tests += 1
                        if expected_result == actual_result:
                            number_correct += 1
                        else:
                            issues.append(f"Test failed: {test_case} Result: {actual_result}")
                            
                    score = 0
                    if total_tests > 0:
                        score = number_correct / total_tests
                    grade = SolutionGrade(problem.identifier, solution.prompt_identifier, solution.model_identifier, score, None, issues)
                    solutionGrades.append(grade)
        return GradingOutput(solutionGrades, self.identifier)

class PerformanceGrader(Grader):
    @classmethod
    @property
    def identifier(self):
        return "performance"
        
    def grade(self, problems: List[ProblemDefinition], solutions: List[LLMSolution]) -> GradingOutput:
        solutionGrades = []
        for problem in problems:
            function_prototype = problem.function_prototype
            for solution in solutions:
                if solution.problem_identifier == problem.identifier:
                    total_solution_time = 0
                    total_optimal_time = 0
                    issues = []
                    for test_case in problem.correctness_test_suite:
                        start_time = time.process_time()
                        Grader.run_function(solution.solution_code, function_prototype, test_case)
                        end_time = time.process_time()
                        total_solution_time += end_time - start_time

                        start_time = time.process_time()
                        Grader.run_function(problem.optimal_solution, function_prototype, test_case)
                        end_time = time.process_time()
                        total_optimal_time += end_time - start_time

                    if total_optimal_time == 0:
                        print("Warning: total_optimal_time is zero! Assigning a default value.")
                        result_ratio = float('inf')
                    else:
                        result_ratio = total_solution_time / total_optimal_time
                    
                    grade = SolutionGrade(problem.identifier, solution.prompt_identifier, solution.model_identifier, result_ratio, None, issues)
                    solutionGrades.append(grade)
        return GradingOutput(solutionGrades, self.identifier)
