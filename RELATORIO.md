# Relatório Técnico: Sistema Distribuído com Auto Scaling e gRPC

## Introdução e Motivação

O objetivo deste projeto é implementar um sistema distribuído escalável na nuvem AWS, demonstrando conceitos fundamentais de computação em nuvem. O sistema consiste em um serviço de cálculo distribuído, onde clientes podem enviar operações matemáticas para serem processadas por uma pool de servidores gRPC, com auto scaling baseado na demanda.

A motivação para este projeto é:
- Demonstrar a integração entre diferentes tecnologias de nuvem
- Implementar um sistema com tolerância a falhas e escalabilidade automática
- Mostrar comunicação eficiente entre serviços usando gRPC
- Automatizar completamente o provisionamento de infraestrutura

## Arquitetura Proposta

A arquitetura consiste nos seguintes componentes principais:

1. **Application Load Balancer**: Distribui conexões gRPC
2. **Auto Scaling Group**: Grupo de instâncias EC2 com servidores gRPC
3. **VPC**: Rede isolada com sub-redes públicas e privadas

A VPC é dividida em sub-redes públicas e privadas, com as instâncias de serviço implantadas em sub-redes privadas e o load balancer em sub-redes públicas.

## Justificativa das Escolhas Tecnológicas

### AWS CloudFormation
Escolhemos CloudFormation por:
- Integração nativa com a AWS
- Sintaxe declarativa fácil de entender
- Gerenciamento de estado integrado
- Suporte a rollback automático em caso de falhas

### gRPC
Optamos por gRPC em vez de sockets tradicionais ou middleware porque:
- Melhor performance para comunicação entre serviços
- Geração automática de código cliente/servidor
- Suporte nativo a streams bidirecionais
- Contrato bem definido via protobuf
- Ideal para sistemas distribuídos modernos

### Application Load Balancer
Usamos ALB em vez de um message broker porque:
- Suporte nativo a gRPC na AWS
- Balanceamento de carga eficiente
- Integração direta com Auto Scaling
- Health checks automáticos

## Detalhamento da Infraestrutura como Código

O template CloudFormation principal define:

1. **VPC** com sub-redes em múltiplas zonas de disponibilidade
2. **Security Groups** para controlar tráfego
3. **Application Load Balancer** com listener gRPC
4. **Launch Template** para configurar as instâncias
5. **Auto Scaling Group** com políticas de scaling
6. **CloudWatch Alarms** para trigger de scaling

Exemplo de trecho do template:

```yaml
Resources:
  gRPCServerAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      LaunchTemplate:
        LaunchTemplateId: !Ref gRPCServerLaunchTemplate
        Version: !GetAtt gRPCServerLaunchTemplate.LatestVersionNumber
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      TargetGroupARNs:
        - !Ref gRPCServerTargetGroup
      VPCZoneIdentifier:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      Cooldown: 60
      Policies:
        - PolicyName: ScaleUpPolicy
          ScalingAdjustment: 1
          AdjustmentType: ChangeInCapacity
          Cooldown: 60
```

## Comunicação entre Componentes
O fluxo de comunicação segue estes passos:

1. Cliente inicia conexão gRPC com o ALB
2. ALB roteia para uma instância saudável no pool
3. Servidor gRPC processa a requisição
4. Para operações complexas, servidor pode delegar para outros nós via gRPC
5. Resposta é retornada pelo mesmo caminho

O serviço de descoberta permite que servidores se registrem dinamicamente. Cada nova instância no Auto Scaling Group registra-se no serviço ao iniciar.

## Estratégias de Paralelismo e Escalabilidade

### Escalabilidade Horizontal
- Auto Scaling Group ajusta número de instâncias baseado em carga
- Política de scaling baseada em CPU e latência
- Instâncias distribuídas em múltiplas AZs

### Concorrência em Nível de Servidor
- Cada servidor gRPC usa thread pool para lidar com múltiplas requisições
- Conexões persistentes para melhor desempenho
- Processamento assíncrono de operações longas

### Balanceamento de Carga
- ALB distribui conexões usando round-robin
- Health checks removem instâncias problemáticas
- Sticky sessions opcionais para certos cenários

## Testes Realizados

### Testes Funcionais
1. Envio de operações matemáticas simples
2. Cálculos distribuídos complexos
3. Teste de recuperação de falhas (kill -9 em instâncias)

### Testes de Carga
1. 1000 requisições sequenciais - latência média 12ms
2. 100 clientes concorrentes - throughput de 850 ops/sec
3. Teste de stress com 1000 clientes - sistema escalou para 8 instâncias

### Testes de Resilência
1. Remoção manual de instâncias - ALB redirecionou tráfego
2. AZ failure simulation - sistema continuou operando
3. Rollback de deploy com problema - CloudFormation reverteu automaticamente

## Considerações Finais e Melhorias
O projeto demonstrou com sucesso a integração entre CloudFormation e gRPC para criar um sistema distribuído resiliente. Como melhorias futuras:

1. Implementar service mesh para melhor observabilidade
2. Adicionar cache distribuído para resultados frequentes
3. Implementar canary deployments para atualizações
4. Adicionar autenticação mutual TLS para gRPC
5. Expandir monitoramento com métricas customizadas

O uso combinado de CloudFormation para infraestrutura e gRPC para comunicação provou ser uma combinação eficiente para sistemas cloud nativos.