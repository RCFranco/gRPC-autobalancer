import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class Calculator(calculator_pb2_grpc.CalculatorServicer):
    def Calculate(self, request, context):
        try:
            op, a, b = request.operation.split()
            a, b = float(a), float(b)
            if op == 'add': result = a + b
            elif op == 'sub': result = a - b
            elif op == 'mul': result = a * b
            elif op == 'div': result = a / b if b != 0 else float('nan')
            return calculator_pb2.CalculationResponse(result=result)
        except:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return calculator_pb2.CalculationResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(Calculator(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()