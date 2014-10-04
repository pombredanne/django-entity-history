from datetime import datetime

from django.test import TestCase
from django_dynamic_fixture import G
from entity.models import Entity

from entity_history import EntityActivationEvent


class EntityActivationTest(TestCase):
    """
    Tests that entity activation events are properly created when entities
    are activated and deactivated.
    """
    def test_entity_creation_activated(self):
        t1 = datetime.utcnow()
        e = G(Entity, is_active=True)
        t2 = datetime.utcnow()

        event = EntityActivationEvent.objects.get()
        self.assertTrue(event.was_activated)
        self.assertEquals(event.entity, e)
        self.assertTrue(t1 <= event.time <= t2)

    def test_entity_creation_deactivated(self):
        t1 = datetime.utcnow()
        e = G(Entity, is_active=False)
        t2 = datetime.utcnow()

        event = EntityActivationEvent.objects.get()
        self.assertFalse(event.was_activated)
        self.assertEquals(event.entity, e)
        self.assertTrue(t1 <= event.time <= t2)

    def test_update_to_active(self):
        t1 = datetime.utcnow()
        e = G(Entity, is_active=False)
        t2 = datetime.utcnow()
        e.is_active = True
        e.save()
        t3 = datetime.utcnow()

        events = list(EntityActivationEvent.objects.order_by('time', 'id'))
        self.assertFalse(events[0].was_activated)
        self.assertEquals(events[0].entity, e)
        self.assertTrue(t1 <= events[0].time <= t2)

        self.assertTrue(events[1].was_activated)
        self.assertEquals(events[1].entity, e)
        self.assertTrue(t2 <= events[1].time <= t3)
