"""
CrewAI Agents for A/B Testing Statistical Analysis

This module defines three specialized agents for comprehensive A/B testing analysis:
1. Statistical Validator Agent - Validates data quality and test assumptions
2. Hypothesis Testing Agent - Performs statistical significance testing
3. Insights Generator Agent - Generates actionable business insights
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os


class ABTestingCrew:
    """CrewAI implementation for A/B Testing analysis"""

    def __init__(self, model_name="gpt-4o-mini"):
        """Initialize the A/B Testing Crew with three specialized agents"""
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Initialize agents
        self.statistical_validator = self._create_statistical_validator()
        self.hypothesis_tester = self._create_hypothesis_tester()
        self.insights_generator = self._create_insights_generator()

    def _create_statistical_validator(self) -> Agent:
        """
        Agent 1: Statistical Validator
        Validates data quality and test assumptions
        """
        return Agent(
            role="Statistical Validator",
            goal="Validate data quality, check statistical assumptions, and identify potential issues in A/B test data",
            backstory="""You are an expert data validation specialist with deep knowledge of
            statistical requirements for A/B testing. You meticulously check for data quality
            issues, sample size adequacy, variance homogeneity, and other critical assumptions
            that must be met for valid statistical inference.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def _create_hypothesis_tester(self) -> Agent:
        """
        Agent 2: Hypothesis Testing Agent
        Performs statistical significance testing and calculates metrics
        """
        return Agent(
            role="Hypothesis Testing Specialist",
            goal="Conduct rigorous statistical hypothesis testing, calculate confidence intervals, and determine statistical significance",
            backstory="""You are a statistical inference expert specializing in A/B testing
            methodology. You understand the nuances of one-sided vs two-sided tests, Type I
            and Type II errors, p-values, z-scores, and effect sizes. You provide precise
            statistical interpretations while being mindful of common pitfalls like p-hacking
            and multiple testing problems.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def _create_insights_generator(self) -> Agent:
        """
        Agent 3: Insights Generator
        Generates actionable business insights from statistical results
        """
        return Agent(
            role="Business Insights Analyst",
            goal="Translate statistical findings into clear, actionable business recommendations",
            backstory="""You are a business analytics expert who bridges the gap between
            statistical analysis and business decision-making. You excel at contextualizing
            A/B test results, explaining what they mean for the business, and providing
            clear recommendations. You consider practical significance alongside statistical
            significance and always think about real-world implementation.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def create_validation_task(self, data_context: str) -> Task:
        """
        Create a task for the Statistical Validator agent

        Parameters
        ----------
        data_context : str
            Description of the A/B test data including sample sizes, conversion rates, etc.

        Returns
        -------
        Task
            CrewAI Task for data validation
        """
        return Task(
            description=f"""
            Validate the A/B test data and assumptions:

            Data Context:
            {data_context}

            Your validation should cover:
            1. Sample size adequacy (is the sample large enough for reliable inference?)
            2. Data quality checks (missing values, outliers, data integrity)
            3. Assumptions verification (independence, random assignment, etc.)
            4. Potential biases or confounding factors
            5. Any concerns about the validity of statistical tests

            Provide a clear assessment of data quality and readiness for statistical testing.
            """,
            agent=self.statistical_validator,
            expected_output="A comprehensive validation report covering sample size, data quality, assumptions, and any concerns"
        )

    def create_hypothesis_testing_task(self, test_context: str, validation_result: str = "") -> Task:
        """
        Create a task for the Hypothesis Testing agent

        Parameters
        ----------
        test_context : str
            Statistical metrics including conversion rates, p-values, z-scores, etc.
        validation_result : str
            Optional output from validation task to inform testing

        Returns
        -------
        Task
            CrewAI Task for hypothesis testing
        """
        context = f"""
        Test Context:
        {test_context}

        Validation Results:
        {validation_result if validation_result else "Proceed with standard testing"}
        """

        return Task(
            description=f"""
            Perform comprehensive hypothesis testing analysis:

            {context}

            Your analysis should include:
            1. Interpretation of p-value in context of the significance level
            2. Explanation of z-score and what it indicates
            3. Assessment of statistical significance
            4. Discussion of effect size (uplift/lift)
            5. Confidence intervals for the difference
            6. Consideration of Type I and Type II error risks
            7. Power analysis recommendations if needed

            Provide clear statistical conclusions about whether the test shows significant differences.
            """,
            agent=self.hypothesis_tester,
            expected_output="A detailed statistical analysis report with hypothesis test results, significance assessment, and technical interpretations"
        )

    def create_insights_task(self, business_context: str, test_results: str = "") -> Task:
        """
        Create a task for the Insights Generator agent

        Parameters
        ----------
        business_context : str
            Business context including what was tested and why
        test_results : str
            Optional output from hypothesis testing task

        Returns
        -------
        Task
            CrewAI Task for generating insights
        """
        context = f"""
        Business Context:
        {business_context}

        Statistical Results:
        {test_results if test_results else "Based on provided metrics"}
        """

        return Task(
            description=f"""
            Generate actionable business insights:

            {context}

            Your insights should include:
            1. Plain-language summary of what the test results mean
            2. Practical significance vs. statistical significance
            3. Business impact assessment (expected lift, revenue impact, etc.)
            4. Clear recommendation: implement, reject, or continue testing
            5. Potential risks or considerations for implementation
            6. Suggestions for follow-up tests or further investigation
            7. Key takeaways for stakeholders

            Make your recommendations clear, actionable, and business-focused.
            """,
            agent=self.insights_generator,
            expected_output="A business-focused insights report with clear recommendations, impact assessment, and actionable next steps"
        )

    def analyze_ab_test(
        self,
        data_context: str,
        test_context: str,
        business_context: str
    ) -> dict:
        """
        Run the complete A/B test analysis with all three agents

        Parameters
        ----------
        data_context : str
            Description of the test data
        test_context : str
            Statistical metrics and test parameters
        business_context : str
            Business context and objectives

        Returns
        -------
        dict
            Results from all three agents including validation, testing, and insights
        """
        # Create tasks
        validation_task = self.create_validation_task(data_context)
        testing_task = self.create_hypothesis_testing_task(test_context)
        insights_task = self.create_insights_task(business_context)

        # Create crew with sequential task execution
        crew = Crew(
            agents=[
                self.statistical_validator,
                self.hypothesis_tester,
                self.insights_generator
            ],
            tasks=[validation_task, testing_task, insights_task],
            verbose=True
        )

        # Execute the crew
        result = crew.kickoff()

        return {
            "validation": validation_task.output if hasattr(validation_task, 'output') else None,
            "hypothesis_testing": testing_task.output if hasattr(testing_task, 'output') else None,
            "insights": insights_task.output if hasattr(insights_task, 'output') else None,
            "full_result": result
        }

    def quick_analysis(self, metrics: dict) -> str:
        """
        Perform a quick analysis using just the insights generator

        Parameters
        ----------
        metrics : dict
            Dictionary containing A/B test metrics

        Returns
        -------
        str
            Quick insights summary
        """
        context = f"""
        A/B Test Results:
        - Control Group Conversion Rate: {metrics.get('cra', 'N/A')}%
        - Treatment Group Conversion Rate: {metrics.get('crb', 'N/A')}%
        - Uplift: {metrics.get('uplift', 'N/A')}%
        - P-value: {metrics.get('p_value', 'N/A')}
        - Z-score: {metrics.get('z_score', 'N/A')}
        - Significant: {metrics.get('significant', 'N/A')}
        - Sample Size A: {metrics.get('visitors_a', 'N/A')}
        - Sample Size B: {metrics.get('visitors_b', 'N/A')}
        """

        task = self.create_insights_task(
            business_context=context,
            test_results="See metrics above"
        )

        crew = Crew(
            agents=[self.insights_generator],
            tasks=[task],
            verbose=True
        )

        result = crew.kickoff()
        return result
