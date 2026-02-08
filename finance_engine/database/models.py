from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Empresa(Base):
    __tablename__ = 'empresas'
    
    id = Column(Integer, primary_key=True)
    razao_social = Column(String(255), nullable=False)
    cnpj = Column(String(18), unique=True)
    regime_tributario = Column(String(50)) # Simples, Lucro Presumido, Real
    
    funcionarios = relationship("Funcionario", back_populates="empresa")

class Funcionario(Base):
    __tablename__ = 'funcionarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    cargo = Column(String(100))
    salario_base = Column(Numeric(precision=14, scale=2))
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    
    empresa = relationship("Empresa", back_populates="funcionarios")

class SimulacaoFinanceira(Base):
    __tablename__ = 'simulacoes'
    
    id = Column(Integer, primary_key=True)
    tipo = Column(String(50)) # AMORTIZACAO, INVESTIMENTO, PAYROLL
    data_criacao = Column(DateTime, default=datetime.utcnow)
    parametros_entrada = Column(JSON)
    resultados = Column(JSON)
    usuario_ref = Column(String(100)) # ID do usuário que gerou
