import nose.tools

import ckan.new_tests.helpers as helpers
import ckan.new_tests.factories as factories
import ckan.model as model

assert_equals = nose.tools.assert_equals
assert_not_equals = nose.tools.assert_not_equals
ResourceView = model.ResourceView


class TestResourceView(object):
    @classmethod
    def setup_class(cls):
        helpers.reset_db()

    def setup(self):
        model.repo.rebuild_db()

    def test_resource_view_get(self):
        resource_view_id = factories.ResourceView()['id']
        resource_view = ResourceView.get(resource_view_id)

        assert_not_equals(resource_view, None)

    def test_get_count_view_type(self):
        factories.ResourceView(view_type='image')
        factories.ResourceView(view_type='webpage')

        result = ResourceView.get_count_not_in_view_types(['image'])

        assert_equals(result, [('webpage', 1)])

    def test_delete_view_type(self):
        factories.ResourceView(view_type='image')
        factories.ResourceView(view_type='webpage')

        ResourceView.delete_not_in_view_types(['image'])

        result = ResourceView.get_count_not_in_view_types(['image'])
        assert_equals(result, [])

    def test_delete_view_type_doesnt_commit(self):
        factories.ResourceView(view_type='image')
        factories.ResourceView(view_type='webpage')

        ResourceView.delete_not_in_view_types(['image'])
        model.Session.rollback()

        result = ResourceView.get_count_not_in_view_types(['image'])
        assert_equals(result, [('webpage', 1)])

    def test_purging_resource_removes_its_resource_views(self):
        resource_view_dict = factories.ResourceView()
        resource = model.Resource.get(resource_view_dict['resource_id'])

        resource.purge()
        model.repo.commit_and_remove()

        assert_equals(ResourceView.get(resource_view_dict['id']), None)
