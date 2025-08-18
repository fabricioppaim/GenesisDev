from flask import Flask, render_template, jsonify
from models import Project, Environment, Documentation

app = Flask(__name__)

# Dados simulados
projects = [
    Project(  # Projeto original 1
        id=1,
        name="Sistema de Pagamentos",
        description="Plataforma de processamento de transações",
        version="1.2.3",
        repo_url="https://dev.azure.com/company/payments",
        documentation=[
            Documentation("Visão Geral", "1.0", "2025-07-10"),
            Documentation("API Spec", "2.1", "2025-07-15")
        ],
        environments=[
            Environment("Produção", "v1.2.2", "2025-07-20 14:30"),
            Environment("Homologação", "v1.2.3", "2025-07-21 09:15")
        ],
        requirements=[
            {"id": "REQ-001", "title": "Processar cartões", "status": "Implementado"},
            {"id": "REQ-002", "title": "Gerar relatórios", "status": "Em teste"}
        ]
    ),
    Project(  # Projeto original 2
        id=2,
        name="Portal do Cliente",
        version="2.5.0",
        description="Área logada para clientes",
        repo_url="https://dev.azure.com/company/portal",
        documentation=[
            Documentation("Manual do Usuário", "3.2", "2025-07-18")
        ],
        environments=[
            Environment("Produção", "v2.4.1", "2025-07-19 10:00"),
            Environment("Homologação", "v2.5.0", "2025-07-22 15:45")
        ],
        requirements=[]
    ),
    # Adicione os novos projetos abaixo
    Project(
        id=3,
        name="Sistema de Matrículas",
        description="Plataforma para matrículas online de cursos",
        version="3.1.0",
        repo_url="https://dev.azure.com/company/matriculas",
        documentation=[
            Documentation("Manual do Aluno", "2.3", "2025-06-15"),
            Documentation("Fluxo de Matrícula", "1.5", "2025-07-01"),
            Documentation("API Integração", "3.0", "2025-07-18")
        ],
        environments=[
            Environment("Produção", "v3.0.2", "2025-07-22 08:00"),
            Environment("Homologação", "v3.1.0", "2025-07-23 14:15"),
            Environment("Teste", "v3.1.1", "2025-07-24 10:30")
        ],
        requirements=[
            {"id": "MAT-001", "title": "Cadastro de Alunos", "status": "Implementado"},
            {"id": "MAT-002", "title": "Pagamento Online", "status": "Implementado"},
            {"id": "MAT-003", "title": "Emissão de Certificado", "status": "Em teste"},
            {"id": "MAT-004", "title": "Integração com CRM", "status": "Pendente"}
        ]
    ),
    Project(
        id=4,
        name="Portal do Professor",
        description="Área exclusiva para professores com ferramentas de gestão de aulas",
        version="2.5.0",
        repo_url="https://dev.azure.com/company/portal-professor",
        documentation=[
            Documentation("Guia do Professor", "1.2", "2025-05-20"),
            Documentation("API de Chamadas", "2.0", "2025-06-30")
        ],
        environments=[
            Environment("Produção", "v2.4.3", "2025-07-20 09:00"),
            Environment("Homologação", "v2.5.0", "2025-07-25 16:45")
        ],
        requirements=[
            {"id": "PROF-001", "title": "Lançamento de Notas", "status": "Implementado"},
            {"id": "PROF-002", "title": "Controle de Frequência", "status": "Implementado"},
            {"id": "PROF-003", "title": "Planejamento de Aulas", "status": "Em teste"},
            {"id": "PROF-004", "title": "Relatórios Personalizados", "status": "Pendente"}
        ]
    ),
    Project(
        id=5,
        name="App Mobile SENAC",
        description="Aplicativo para alunos acessarem conteúdos e serviços",
        version="1.7.0",
        repo_url="https://dev.azure.com/company/app-mobile",
        documentation=[
            Documentation("Documentação Técnica", "1.0", "2025-04-10"),
            Documentation("Guia de Publicação", "1.2", "2025-07-05"),
            Documentation("Design System", "2.1", "2025-07-12")
        ],
        environments=[
            Environment("Produção (iOS)", "v1.6.2", "2025-07-18 11:00"),
            Environment("Produção (Android)", "v1.6.2", "2025-07-18 11:30"),
            Environment("Homologação", "v1.7.0", "2025-07-26 09:00"),
            Environment("Teste", "v1.7.1", "2025-07-27 14:00")
        ],
        requirements=[
            {"id": "APP-001", "title": "Login com Redes Sociais", "status": "Implementado"},
            {"id": "APP-002", "title": "Notificações Push", "status": "Implementado"},
            {"id": "APP-003", "title": "Player de Vídeos", "status": "Em teste"},
            {"id": "APP-004", "title": "Offline Mode", "status": "Pendente"},
            {"id": "APP-005", "title": "Integração com LMS", "status": "Pendente"}
        ]
    ),
    Project(
        id=6,
        name="Sistema de Biblioteca",
        description="Gestão de acervo e empréstimos de materiais didáticos",
        version="4.2.0",
        repo_url="https://dev.azure.com/company/biblioteca",
        documentation=[
            Documentation("Manual do Bibliotecário", "3.1", "2025-03-15"),
            Documentation("Termos de Uso", "1.0", "2025-06-22")
        ],
        environments=[
            Environment("Produção", "v4.1.3", "2025-07-15 10:00"),
            Environment("Homologação", "v4.2.0", "2025-07-28 13:20")
        ],
        requirements=[
            {"id": "BIB-001", "title": "Cadastro de Acervo", "status": "Implementado"},
            {"id": "BIB-002", "title": "Controle de Empréstimos", "status": "Implementado"},
            {"id": "BIB-003", "title": "Renovação Online", "status": "Implementado"},
            {"id": "BIB-004", "title": "Reserva de Materiais", "status": "Em teste"},
            {"id": "BIB-005", "title": "Integração com RFID", "status": "Pendente"}
        ]
    )
]

@app.route('/')
def dashboard():
    return render_template('dashboard.html', projects=projects)

@app.route('/project/<int:project_id>')
def project_details(project_id):
    project = next((p for p in projects if p.id == project_id), None)
    return render_template('project.html', project=project)

@app.route('/api/projects')
def projects_api():
    return jsonify([p.to_dict() for p in projects])

if __name__ == '__main__':
    app.run(debug=True)