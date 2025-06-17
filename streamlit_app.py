import streamlit as st
import openai
import re
from typing import Dict, List

# Configure OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Add to Streamlit secrets


class StrategyExplainer:
    def __init__(self):
        self.system_prompt = """
You are an expert trading strategy analyst. Your job is to analyze NinjaScript trading strategies and explain them in clear, plain English.

For any strategy code provided, you should:
1. Identify the core trading logic
2. Explain entry and exit conditions
3. Describe risk management rules
4. Highlight key parameters
5. Assess the strategy's approach (momentum, mean reversion, etc.)
6. Point out potential strengths and weaknesses

Format your response as:
- **Strategy Type**: [Brief classification]
- **Entry Conditions**: [When trades are opened]
- **Exit Conditions**: [When trades are closed]
- **Risk Management**: [Stop losses, position sizing, etc.]
- **Key Parameters**: [Important configurable values]
- **Assessment**: [Strengths and potential concerns]
- **Plain English Summary**: [2-3 sentence explanation anyone could understand]
"""

    def analyze_strategy(self, strategy_code: str) -> Dict[str, str]:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Analyze this NinjaScript strategy:\n\n{strategy_code}"}
                ],
                max_tokens=1500,
                temperature=0.3
            )

            return {
                "analysis": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "cost_estimate": response.usage.total_tokens * 0.00003  # GPT-4 pricing
            }
        except Exception as e:
            return {"error": str(e)}

    def extract_parameters(self, strategy_code: str) -> List[Dict[str, str]]:
        """Extract configurable parameters from NinjaScript code"""
        parameters = []

        # Find property declarations
        property_pattern = r'public\s+(\w+)\s+(\w+)\s*{\s*get;\s*set;\s*}'
        matches = re.findall(property_pattern, strategy_code)

        for param_type, param_name in matches:
            # Look for default values in SetDefaults
            default_pattern = rf'{param_name}\s*=\s*([^;]+);'
            default_match = re.search(default_pattern, strategy_code)
            default_value = default_match.group(1) if default_match else "Not found"

            parameters.append({
                "name": param_name,
                "type": param_type,
                "default_value": default_value
            })

        return parameters


def main():
    st.set_page_config(
        page_title="AI Strategy Explainer",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 AI Strategy Explainer")
    st.subtitle("Transform complex NinjaScript strategies into plain English")

    # Sidebar for demo strategies
    with st.sidebar:
        st.header("📊 Demo Strategies")
        if st.button("Load Sample Strategy"):
            # You can add your actual strategy here
            sample_strategy = """
            // Sample simplified strategy for demo
            public class SimpleMAStrategy : Strategy
            {
                public int FastMA { get; set; } = 10;
                public int SlowMA { get; set; } = 20;
                public int StopLoss { get; set; } = 50;

                protected override void OnBarUpdate()
                {
                    if (CrossAbove(EMA(FastMA), EMA(SlowMA), 1))
                        EnterLong();
                    if (CrossBelow(EMA(FastMA), EMA(SlowMA), 1))
                        EnterShort();
                }
            }
            """
            st.session_state.strategy_code = sample_strategy

    # Main interface
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Strategy Code Input")
        strategy_code = st.text_area(
            "Paste your NinjaScript strategy here:",
            value=st.session_state.get('strategy_code', ''),
            height=400,
            placeholder="Paste your NinjaScript strategy code here..."
        )

        if st.button("🚀 Analyze Strategy", type="primary"):
            if strategy_code.strip():
                with st.spinner("AI is analyzing your strategy..."):
                    explainer = StrategyExplainer()
                    result = explainer.analyze_strategy(strategy_code)

                    if "error" in result:
                        st.error(f"Analysis failed: {result['error']}")
                    else:
                        st.session_state.analysis_result = result
                        st.session_state.parameters = explainer.extract_parameters(strategy_code)
                        st.success("Analysis complete!")
            else:
                st.warning("Please paste a strategy first!")

    with col2:
        st.header("🧠 AI Analysis")

        if 'analysis_result' in st.session_state:
            result = st.session_state.analysis_result

            # Show analysis
            st.markdown(result["analysis"])

            # Show extracted parameters
            if 'parameters' in st.session_state and st.session_state.parameters:
                st.subheader("⚙️ Extracted Parameters")
                params_df = st.dataframe(st.session_state.parameters)

            # Show usage stats
            with st.expander("📈 Analysis Stats"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Tokens Used", result["tokens_used"])
                with col_b:
                    st.metric("Cost", f"${result['cost_estimate']:.4f}")
        else:
            st.info("👈 Paste a strategy and click 'Analyze' to see the AI explanation")

    # Footer
    st.markdown("---")
    st.markdown("""
    **🎯 Coming Next Week:** Code Cleaner Agent - Automatically optimize and improve your strategy code!

    **📧 Want early access?** [Join the waitlist](https://your-landing-page.com)
    """)


if __name__ == "__main__":
    main()