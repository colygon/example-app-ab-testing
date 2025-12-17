# CrewAI Upgrade Documentation

## Overview

This document describes the CrewAI integration added to the A/B Testing Streamlit app. The upgrade enhances the original statistical analysis capabilities with AI-powered insights from specialized agents.

**Upgrade Date:** December 17, 2025
**Agent ID:** Agent 32
**CrewAI Version:** >=0.86.0

## What's New

### AI-Powered Statistical Analysis

The upgraded application now features three specialized AI agents that work together to provide comprehensive A/B test analysis:

#### 1. Statistical Validator Agent
- **Role:** Validates data quality and statistical assumptions
- **Capabilities:**
  - Checks sample size adequacy
  - Identifies data quality issues
  - Verifies statistical test assumptions
  - Flags potential biases or confounding factors
  - Assesses data readiness for statistical inference

#### 2. Hypothesis Testing Specialist Agent
- **Role:** Performs rigorous statistical significance testing
- **Capabilities:**
  - Interprets p-values in context
  - Explains z-scores and their implications
  - Assesses statistical significance
  - Analyzes effect sizes (uplift/lift)
  - Calculates confidence intervals
  - Discusses Type I and Type II error risks
  - Provides power analysis recommendations

#### 3. Business Insights Analyst Agent
- **Role:** Translates statistical findings into actionable business recommendations
- **Capabilities:**
  - Provides plain-language summaries
  - Distinguishes practical vs. statistical significance
  - Assesses business impact
  - Makes clear implementation recommendations
  - Identifies risks and considerations
  - Suggests follow-up tests
  - Delivers stakeholder-ready insights

## Architecture

### File Structure

```
abtesting-agent32/
├── streamlit_app.py          # Main Streamlit application (upgraded)
├── crew_agents.py             # NEW: CrewAI agents and tasks
├── requirements.txt           # Updated with CrewAI dependencies
├── CREWAI_UPGRADE.md         # This file
├── README.md                  # Original README
├── Website_Results.csv        # Example data
├── ab_data.csv               # Example data
└── streamlit_app_sk.py       # Alternative implementation
```

### Key Components

#### ABTestingCrew Class (`crew_agents.py`)

The main class that orchestrates all three agents:

```python
class ABTestingCrew:
    - __init__(): Initializes LLM and creates three agents
    - _create_statistical_validator(): Creates validation agent
    - _create_hypothesis_tester(): Creates testing agent
    - _create_insights_generator(): Creates insights agent
    - create_validation_task(): Task for data validation
    - create_hypothesis_testing_task(): Task for statistical testing
    - create_insights_task(): Task for business insights
    - analyze_ab_test(): Runs complete multi-agent analysis
    - quick_analysis(): Runs quick insights-only analysis
```

#### Integration in Streamlit (`streamlit_app.py`)

The CrewAI features are seamlessly integrated into the existing Streamlit interface:

1. **Quick Analysis Button:** Generates rapid AI insights using the Business Insights Analyst
2. **Detailed Analysis Expander:** Runs all three agents sequentially for comprehensive analysis
3. **Error Handling:** Graceful degradation if API key is missing or errors occur
4. **User Feedback:** Spinners and status messages during analysis

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/example-app-ab-testing.git
   cd example-app-ab-testing
   git checkout crewai-upgrade
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key:**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage Guide

### Basic Workflow

1. **Upload Data or Use Example:**
   - Upload your A/B test CSV file, or
   - Check "Use example file" to try with sample data

2. **Configure Test:**
   - Select A/B column and Result column
   - Adjust hypothesis type (one-sided/two-sided)
   - Set significance level (α)

3. **View Standard Results:**
   - Conversion rates for both groups
   - Statistical metrics (p-value, z-score, uplift)
   - Significance assessment
   - Visualization charts

4. **Generate AI Analysis:**
   - Click "Generate AI Analysis" button
   - Wait for the Business Insights Analyst to provide recommendations
   - Review AI-generated insights

5. **Run Detailed Analysis (Optional):**
   - Expand "Run Detailed Multi-Agent Analysis"
   - Click "Run Detailed Analysis"
   - Review reports from all three agents:
     - Validation Report
     - Hypothesis Testing Analysis
     - Business Insights

### Example Output

The AI agents provide structured output including:

- **Data Quality Assessment:** Sample size evaluation, data integrity checks
- **Statistical Interpretation:** P-value meaning, z-score explanation, significance context
- **Business Recommendations:** Clear go/no-go decisions, risk assessment, next steps
- **Plain-Language Summaries:** Non-technical explanations for stakeholders

## Dependencies

### New Dependencies Added

```
crewai>=0.86.0              # Multi-agent orchestration framework
langchain-openai>=0.3.0     # OpenAI integration for LangChain
python-dotenv>=1.0.0        # Environment variable management
```

### Existing Dependencies

```
streamlit==1.16.0           # Web application framework
numpy==1.19.5               # Numerical computing
altair==4.1.0               # Declarative visualization
pandas==1.2.5               # Data manipulation
scipy==1.6.2                # Scientific computing
click==8                    # Command-line interface
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required for AI agent functionality
- Model used: `gpt-4o-mini` (configurable in `ABTestingCrew.__init__()`)

### Agent Configuration

Agents can be customized by modifying `crew_agents.py`:

- **Temperature:** Adjust `temperature` parameter in `ChatOpenAI` (default: 0.1)
- **Model:** Change `model_name` in `ABTestingCrew.__init__()` (default: "gpt-4o-mini")
- **Verbosity:** Toggle `verbose` flag in Agent definitions
- **Backstory:** Modify agent backstories to change behavior and expertise

## Advanced Usage

### Programmatic Access

You can use the CrewAI agents programmatically:

```python
from crew_agents import ABTestingCrew

# Initialize crew
crew = ABTestingCrew(model_name="gpt-4o-mini")

# Prepare metrics
metrics = {
    'cra': 5.2,
    'crb': 6.8,
    'uplift': 30.77,
    'p_value': 0.001,
    'z_score': 3.2,
    'significant': 'YES',
    'visitors_a': 10000,
    'visitors_b': 10000,
    'conversions_a': 520,
    'conversions_b': 680
}

# Quick analysis
insights = crew.quick_analysis(metrics)
print(insights)

# Full analysis
results = crew.analyze_ab_test(
    data_context="Your data description",
    test_context="Your test metrics",
    business_context="Your business context"
)
```

### Custom Tasks

Create custom tasks for specific analysis needs:

```python
from crewai import Task

custom_task = Task(
    description="Analyze seasonal trends in conversion rates",
    agent=crew.insights_generator,
    expected_output="Seasonal trend analysis report"
)
```

## Limitations and Considerations

1. **API Costs:** Each AI analysis makes API calls to OpenAI, which incur costs
2. **Response Time:** AI analysis takes 10-30 seconds depending on complexity
3. **API Key Required:** Without OPENAI_API_KEY, AI features are disabled (app still works for standard analysis)
4. **Internet Connection:** Required for API calls to OpenAI
5. **Rate Limits:** Subject to OpenAI API rate limits

## Troubleshooting

### Common Issues

**Issue:** "OpenAI API key not found" warning
- **Solution:** Set the `OPENAI_API_KEY` environment variable

**Issue:** Import error for crewai
- **Solution:** Run `pip install -r requirements.txt` to install all dependencies

**Issue:** Analysis takes too long
- **Solution:** Use quick analysis instead of detailed analysis, or check internet connection

**Issue:** API rate limit errors
- **Solution:** Wait a few moments and try again, or upgrade OpenAI API plan

## Migration from Original App

The upgrade is **backward compatible**. The original functionality remains unchanged:

- All original features work exactly as before
- AI features are **additive** - they don't modify existing calculations
- You can use the app without setting up CrewAI (AI section won't show)
- Original data files work without modification

## Future Enhancements

Potential improvements for future versions:

1. **Additional Agents:**
   - Experiment design advisor
   - Sample size calculator
   - Multi-variate testing specialist

2. **Enhanced Features:**
   - Historical test comparison
   - Bayesian A/B testing
   - Sequential testing support
   - Effect size visualization

3. **Integration Options:**
   - Export AI reports to PDF
   - Slack/email notifications
   - API endpoint for programmatic access
   - Database integration for test history

## Technical Details

### Agent Communication Flow

```
User Input → Streamlit UI → ABTestingCrew
                                  ↓
                     ┌────────────┴────────────┐
                     ↓                         ↓
              Quick Analysis            Detailed Analysis
                     ↓                         ↓
           Insights Agent Only      All Three Agents (Sequential)
                     ↓                         ↓
                     │         1. Validation Agent
                     │         2. Hypothesis Agent
                     │         3. Insights Agent
                     ↓                         ↓
              Display Results          Display All Reports
```

### Task Execution Model

- **Quick Analysis:** Single agent, single task (~10-15 seconds)
- **Detailed Analysis:** Three agents, three tasks, sequential execution (~30-45 seconds)
- Tasks are executed using CrewAI's `kickoff()` method
- Results are stored in task output attributes

## Contributing

To contribute improvements to the CrewAI integration:

1. Create a feature branch from `crewai-upgrade`
2. Make your modifications to `crew_agents.py` or `streamlit_app.py`
3. Test thoroughly with example data
4. Submit a pull request with clear description

## Credits

- **Original App:** Streamlit team (https://github.com/streamlit/example-app-ab-testing)
- **CrewAI Integration:** Agent 32
- **Framework:** CrewAI (https://github.com/joaomdmoura/crewAI)
- **LLM Provider:** OpenAI

## License

This project maintains the original license from the upstream repository. CrewAI integration is provided as-is for educational and commercial use.

## Support

For issues related to:
- **Original app functionality:** See original repository
- **CrewAI integration:** Open an issue in this fork
- **CrewAI framework:** See CrewAI documentation
- **OpenAI API:** See OpenAI documentation

## Version History

### v2.0.0 - CrewAI Upgrade (December 17, 2025)
- Added three specialized AI agents
- Integrated CrewAI for multi-agent orchestration
- Added quick and detailed analysis modes
- Updated dependencies (crewai>=0.86.0, langchain-openai>=0.3.0)
- Created comprehensive documentation

### v1.0.0 - Original App
- Basic A/B testing statistical analysis
- Streamlit interface
- CSV upload and example data
- Visualization with Altair

---

**Upgraded by Agent 32** | December 17, 2025
