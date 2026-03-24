# agents.py 

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains import RetrievalQA
import os

# Import Ollama from the new package
try:
    from langchain_ollama import OllamaLLM
except ImportError:
    # Fallback for old version
    from langchain_community.llms import Ollama as OllamaLLM

# Import from the new package
try:
    from langchain_chroma import Chroma
except ImportError:
    # Fallback for old version
    from langchain_community.vectorstores import Chroma

# Import embeddings
try:
    from langchain_ollama import OllamaEmbeddings
except ImportError:
    # Fallback for old version
    from langchain_community.embeddings import OllamaEmbeddings

class AgentsSystem:
    def __init__(self):
        # Initialize the LLM for all agents - Use new OllamaLLM
        try:
            self.llm = OllamaLLM(base_url="http://localhost:11434", model="llama3")
        except Exception as e:
            print(f"Error initializing Ollama: {e}")
            print("Please ensure Ollama is running on http://localhost:11434")
            raise
        
        # Initialize vector database for RAG with company data
        try:
            embeddings = OllamaEmbeddings(model="llama3", base_url="http://localhost:11434")
            self.vector_db = Chroma(
                persist_directory="./chroma_db_company",
                embedding_function=embeddings
            )
            print("  Vector database loaded successfully")
        except Exception as e:
            print(f"Error initializing vector database: {e}")
            raise
        
        # Configure retriever
        self.retriever = self.vector_db.as_retriever(
            search_kwargs={
                "k": 5  # Only keep the k parameter
            }
        )
        
        # Initialize agents
        self._setup_onboarding_agent()
        self._setup_learning_agent()
        self._setup_coach_agent()
        self._setup_concierge_agent()
    
    def _setup_onboarding_agent(self):
        """Setup onboarding assistant agent"""
        onboarding_prompt_template = """I am a professional onboarding assistant specialized in answering questions about company policies, procedures, and related information.

Please answer strictly based on the following company document content. If the information is not available in the documents, please state so honestly.

Relevant document content:
{context}

Question: {question}

Please provide accurate, detailed answers and cite information sources when possible. Maintain professionalism and accuracy in your responses.

Professional response:"""
        
        onboarding_prompt = PromptTemplate(
            template=onboarding_prompt_template,
            input_variables=["context", "question"]
        )
        
        self.onboarding_agent = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": onboarding_prompt},
            return_source_documents=True
        )
    
    def _setup_learning_agent(self):
        """Setup learning companion agent - Updated to use LCEL instead of LLMChain"""
        learning_prompt = PromptTemplate(
            template="""I am a helpful and inspiring learning companion for young professionals.
My goal is to suggest relevant learning resources, courses, books, or internal workshops based on the user's role and interests.

Role: {role}
Interests: {interests}
Query: {query}

Provide friendly, motivating responses with 2-3 concrete suggestions. I can recommend based on training resources found in company documents.

Learning Companion:""",
            input_variables=["role", "interests", "query"]
        )
        
        # Replace LLMChain with LCEL
        self.learning_agent = (
            learning_prompt 
            | self.llm 
            | StrOutputParser()
        )
    
    def _setup_coach_agent(self):
        """Setup career coach agent - Updated to use LCEL instead of LLMChain"""
        coach_prompt = PromptTemplate(
            template="""I am an experienced career coach. My role is to provide guidance on goal setting, skill development for career advancement, and navigating company culture.

Query: {query}

Provide thoughtful, actionable advice. Ask clarifying questions if the query is vague. I can reference relevant career development paths from company policies.

Career Coach:""",
            input_variables=["query"]
        )
        
        # Replace LLMChain with LCEL
        self.coach_agent = (
            coach_prompt 
            | self.llm 
            | StrOutputParser()
        )
    
    def _setup_concierge_agent(self):
        """Setup concierge routing agent"""
        destinations = [
            {
                "name": "onboarding", 
                "description": "Good for questions about company policies, HR, IT setup, team structures, onboarding procedures, office processes."
            },
            {
                "name": "learning", 
                "description": "Good for questions about learning, skill development, course recommendations, training resources, professional knowledge enhancement."
            },
            {
                "name": "career_coach", 
                "description": "Good for questions about career growth, goal setting, performance reviews, long-term development, promotion paths."
            }
        ]
        
        destinations_str = "\n".join([f"{d['name']}: {d['description']}" for d in destinations])
        
        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser()
        )
        self.concierge_agent = LLMRouterChain.from_llm(self.llm, router_prompt)
    
    def process_query(self, user_query, user_data):
        """Process user query"""
        try:
            # Updated to use the new API for routing
            route = self.concierge_agent.invoke({"input": user_query})
            next_step = route["destination"].lower()
        except Exception as e:
            print(f"Routing error: {e}")
            next_step = "onboarding"  # Default route to onboarding assistant
        
        response_data = {
            "answer": "",
            "agent_name": "",
            "sources": []
        }
        
        if next_step == "onboarding":
            try:
                result = self.onboarding_agent.invoke({"query": user_query})
                response_data["answer"] = result['result']
                response_data["agent_name"] = "  Company Document Assistant"
                # Extract source document information
                if hasattr(result, 'source_documents') and result['source_documents']:
                    response_data["sources"] = [
                        doc.metadata.get('filename', 'Unknown file') 
                        for doc in result['source_documents']
                    ]
            except Exception as e:
                print(f"Onboarding agent error: {e}")
                response_data["answer"] = "I encountered an error while searching our documents. Please try again or ask a different question."
                response_data["agent_name"] = "  Company Document Assistant"
        
        elif next_step == "learning":
            try:
                # Updated to invoke the new LCEL chain
                response = self.learning_agent.invoke({
                    "role": user_data.get('role', ''),
                    "interests": user_data.get('interests', ''),
                    "query": user_query
                })
                response_data["answer"] = response  # LCEL returns string directly
                response_data["agent_name"] = "  Learning Companion"
            except Exception as e:
                print(f"Learning agent error: {e}")
                response_data["answer"] = "I had trouble processing your learning request. Please try again."
                response_data["agent_name"] = "  Learning Companion"
        
        elif next_step == "career_coach":
            try:
                # Updated to invoke the new LCEL chain
                response = self.coach_agent.invoke({"query": user_query})
                response_data["answer"] = response  # LCEL returns string directly
                response_data["agent_name"] = "  Career Coach"
            except Exception as e:
                print(f"Career coach error: {e}")
                response_data["answer"] = "I encountered an issue with career guidance. Please try again."
                response_data["agent_name"] = "  Career Coach"
        
        else:
            response_data["answer"] = "I'm not sure how to answer this question. Please try rephrasing your question or specify whether you need help with onboarding, learning, or career development."
            response_data["agent_name"] = "  Assistant"
        
        return response_data

# Global instance
agents_system = AgentsSystem()