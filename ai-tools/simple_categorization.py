import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import logfire
    import nest_asyncio

    from typing import Literal

    from pydantic import BaseModel, Field, AliasChoices
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from pydantic_ai import Agent
    from pydantic_ai.models.anthropic import AnthropicModel
    from pydantic_ai.providers.anthropic import AnthropicProvider

    logfire.configure()  
    logfire.instrument_pydantic_ai()  
    logfire.instrument_httpx(capture_all=True)  
    return (
        Agent,
        AliasChoices,
        AnthropicModel,
        AnthropicProvider,
        BaseModel,
        BaseSettings,
        Field,
        Literal,
        SettingsConfigDict,
        nest_asyncio,
    )


@app.cell
def _(AliasChoices, BaseSettings, Field, SettingsConfigDict):
    class AIConfig(BaseSettings):
        api_key: str = Field(
            description="The Anthropic API Key",
            validation_alias=AliasChoices("api_key", "anthropic_api_key")
        )

        model_config = SettingsConfigDict(env_file=".env")

    config = AIConfig()
    return (config,)


@app.cell
def _(
    Agent,
    AnthropicModel,
    AnthropicProvider,
    BaseModel,
    Field,
    Literal,
    config,
    nest_asyncio,
):
    data = [
        {
            "date": "2025-07-29",
            "amount" : -8.4,
            "remitter_name": "VINZENZ MURR VERTIEBS",
            "remitter_info": "01VINZENZ MURR VERTIEBS, MUENCHEN DE02Karte Nr. 4871 78XX XXXX 5504 03Kartenzahlung 04comdirect Visa-Debitkarte 052025-07-25 00:00:00",
            "transaction_type": "DIRECT_DEBIT"
        },
        {
            "date": "2025-07-29",
            "amount" : -20.37,
            "remitter_name": "Aumeister OHG",
            "remitter_info": "01Aumeister OHG, Muenchen DE 02Karte Nr. 4871 78XX XXXX 5504 03Kartenzahlung 04comdirect Visa-Debitkarte 052025-07-27 00:00:00",
            "transaction_type": "DIRECT_DEBIT"
        },
        {
            "date": "2025-07-28",
            "amount" : -109.99,
            "remitter_name": "REWE Muenchen Boge",
            "remitter_info": "01REWE Muenchen Boge, Muenchen DE 02Karte Nr. 4871 78XX XXXX 5504 03Kartenzahlung 04comdirect Visa-Debitkarte 052025-07-25 00:00:00",
            "transaction_type": "DIRECT_DEBIT"
        },
        {
            "date": "2025-07-25",
            "amount" : 152.49,
            "remitter_name": "LUFTHANSA   2202229932496",
            "remitter_info": "01LUFTHANSA 2202229932496, KOLN DE02Karte Nr. 4871 78XX XXXX 5504 03Kartenzahlung 04comdirect Visa-Debitkarte 052025-07-22 00:00:00",
            "transaction_type": "TRANSFER"
        }
    ]

    class TransactionCategorization(BaseModel):
        improved_description: str = Field(description="The improved description of the transaction")
        category: Literal["Groceries", "Travel", "Restaurant"]

    # To fix 'This event loop is already running' RuntimeError
    nest_asyncio.apply()

    bank_model = AnthropicModel(
        "claude-3-5-sonnet-latest",
        provider=AnthropicProvider(api_key=config.api_key)
    )
    bank_agent = Agent(
        model=bank_model,
        system_prompt="""
        You are a very knowledgeable personal finance assistant.
        Your speciality lies in: 
          * determening the category of a financial transactions
          * providing a consice description of a financial transaction better than the original
        given the details of the transactions.
        """,
        output_type=TransactionCategorization
    )

    # To fix 'This event loop is already running' RuntimeError
    nest_asyncio.apply()

    for transaction in data:
        result = bank_agent.run_sync(f"Transaction: '{transaction}'")
        print(result.output)

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
