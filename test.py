from application import IrisInputData, kafka_app, IrisPrediction

from fastkafka.testing import Tester

msg = IrisInputData(
    sepal_length=0.1,
    sepal_width=0.2,
    petal_length=0.3,
    petal_width=0.4,
)

async def test_using_inmemory_kafka_broker():
    # Start Tester app and create InMemory Kafka broker for testing
    async with Tester(kafka_app) as tester:
        # Send IrisInputData message to input_data topic
        await tester.to_input_data(msg)

        # Assert that the kafka_app responded with IrisPrediction in predictions topic
        await tester.awaited_mocks.on_predictions.assert_awaited_with(
            IrisPrediction(species="setosa"), timeout=2
        )

async def test_using_apache_kafka_broker():
    # Start Tester app and create InMemory Kafka broker for testing
    async with Tester(kafka_app).using_local_kafka() as tester:
        # Send IrisInputData message to input_data topic
        await tester.to_input_data(msg)

        # Assert that the kafka_app responded with IrisPrediction in predictions topic
        await tester.awaited_mocks.on_predictions.assert_awaited_with(
            IrisPrediction(species="setosa"), timeout=2
        )

import asyncio
asyncio.run(test_using_inmemory_kafka_broker())
asyncio.run(test_using_apache_kafka_broker())
