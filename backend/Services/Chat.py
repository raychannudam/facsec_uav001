from sqlalchemy.orm import Session
from Models.Chat import ChatMessageModel, ChatConversationModel, ChatSessionModel
from Schemas.Chat import ChatMessageCreateSchema
from Agent.agent import get_agent

class ChatService:

    @staticmethod
    def create_chat_session(user_id: int, db: Session) -> ChatSessionModel:
        session = ChatSessionModel(user_id=user_id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_chat_session(session_id: int, db: Session) -> ChatSessionModel:
        return db.query(ChatSessionModel).filter(ChatSessionModel.id == session_id).first()

    @staticmethod
    def create_chat_conversation(session_id: int, user_id: int, db: Session, name: str = "New Conversation") -> ChatConversationModel:
        conversation = ChatConversationModel(session_id=session_id, user_id=user_id, name=name)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def get_chat_conversation(conversation_id: int, db: Session) -> ChatConversationModel:
        return db.query(ChatConversationModel).filter(ChatConversationModel.id == conversation_id).first()

    @staticmethod
    def create_chat_message(conversation_id: int, user_id: int, user_prompt: str, db: Session) -> ChatMessageModel:
        agent_executor = get_agent()

        # 🔥 Pass db session to tools through config
        response = agent_executor.invoke({
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        })
        ai_messages = [msg for msg in response["messages"] if hasattr(msg, 'content') and msg.content]
        if ai_messages:
            bot_response = ai_messages[-1].content
        else:
            bot_response = "No AI response generated"
        

        message = ChatMessageModel(
            conversation_id=conversation_id,
            user_id=user_id,
            user_prompt=user_prompt,
            response=bot_response
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_messages_by_conversation(conversation_id: int, db: Session) -> list[ChatMessageModel]:
        conversation = db.query(ChatConversationModel).filter(ChatConversationModel.id == conversation_id).first()
        if not conversation:
            return []
        return conversation.messages
