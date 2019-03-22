from django.db import models


class Node(models.Model):
    node_id = models.PositiveIntegerField()
    moisture = models.DecimalField(decimal_places=1, max_digits=5)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.node_id)
