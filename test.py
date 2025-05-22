import logging
import turtle

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Create a turtle object
logging.info("Creating turtle...")
t = turtle.Turtle()

# Draw a square
logging.info("Drawing a square...")
for _ in range(4):
    t.forward(100)
    t.right(90)

logging.info("Finished drawing!")
turtle.done()
