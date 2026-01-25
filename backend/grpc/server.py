from concurrent import futures
import grpc

import trainer_pb2
import trainer_pb2_grpc


class TrainerService(trainer_pb2_grpc.TrainerServiceServicer):

    def Retrain(self, request, context):
        json_payload = request.json_payload

        try:
            print("Received retrain request")
            print(json_payload[:500])  # preview first 500 chars

            # TODO: hook LoRA / RAG retraining here

            return trainer_pb2.RetrainResponse(
                success=True,
                message="Retraining started successfully"
            )

        except Exception as e:
            return trainer_pb2.RetrainResponse(
                success=False,
                message=str(e)
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    trainer_pb2_grpc.add_TrainerServiceServicer_to_server(
        TrainerService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("gRPC Trainer Server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
