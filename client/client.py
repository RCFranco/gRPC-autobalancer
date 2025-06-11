import grpc
import calculator_pb2
import calculator_pb2_grpc
import argparse

def run(host, operation):
    channel = grpc.insecure_channel(f'{host}:50051', options=[('grpc.enable_https_proxy', 0)])
    stub = calculator_pb2_grpc.CalculatorStub(channel)
    response = stub.Calculate(calculator_pb2.CalculationRequest(operation=operation))
    print(f"Result: {response.result}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--alb-dns', required=True)
    parser.add_argument('--operation', required=True)
    args = parser.parse_args()
    run(args.alb_dns, args.operation)
