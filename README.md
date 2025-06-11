# Sistema Distribuído com Auto Scaling e gRPC
Este projeto implementa um serviço de cálculo distribuído escalável na AWS, usando CloudFormation para infraestrutura e gRPC para comunicação entre serviços.

## Membros
- Rodrigo Franco
- Fabio Monteiro
- Enzo Martins

## Pré-requisitos
- AWS CLI configurado
- Conta AWS com permissões adequadas
- Python 3.7+
- git

## Estrutura do Projeto

```
grpc-autobalancer/
├── cloudformation/
│ └── infra.yml         # Template único de infraestrutura
├── protos/
│ └── calculator.proto  # Contrato gRPC
├── server/
│ └── server.py         # Servidor gRPC
├── client/
│ └── client.py         # Cliente de teste
└── requirements.txt
```

## Implantação da Infraestrutura

1. Crie a infraestrutura:
```bash
aws cloudformation deploy \
    --template-file cloudformation/infra.yml \
    --stack-name GrpcSystem \
    --capabilities CAPABILITY_IAM
```

2. Obtenha o DNS do ALB:
```bash
aws cloudformation describe-stacks \
    --stack-name GrpcSystem \
    --query "Stacks[0].Outputs[?OutputKey=='ALBDNS'].OutputValue" \
    --output text
```

3. Execute o cliente:
```bash
cd client
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python client.py --alb-dns [DNS_DO_ALB] --operation "add 5 3"
```

## Configurações Personalizadas
É possível ajustar parâmetros como:

- Tamanho das instâncias EC2
- Políticas de auto scaling
- Regiões AWS
- Portas gRPC

Edite os arquivos YAML em cloudformation/ antes da implantação.

## Solução de Problemas

### Conexões gRPC falhando
- Verifique se os security groups permitem tráfego na porta gRPC (50051 por padrão)
- Confirme se o ALB está usando o protocolo gRPC

### Auto Scaling não funcionando
- Verifique as métricas do CloudWatch
- Confirme as políticas de IAM para o Auto Scaling
- Verifique os health checks do ALB

### Alta Latência
- Aumente o tamanho das instâncias
- Considere usar gRPC com keep-alive
- Verifique a localização geográfica dos recursos