import json
import demistomock as demisto
from GetOnCallHoursPerUser import main

ROLES = [
    {
        'name': 'Shift1',
        'shifts': [
            {'fromDay': 0, 'fromHour': 8, 'fromMinute': 0, 'toDay': 3, 'toHour': 12, 'toMinute': 0},
            {'fromDay': 4, 'fromHour': 16, 'fromMinute': 0, 'toDay': 6, 'toHour': 20, 'toMinute': 0}
        ]
    },
    {
        'name': 'Administrator',
        'shifts': None
    },
    {
        'name': 'Shift2',
        'shifts': [
            {'fromDay': 0, 'fromHour': 8, 'fromMinute': 0, 'toDay': 3, 'toHour': 12, 'toMinute': 0},
            {'fromDay': 4, 'fromHour': 16, 'fromMinute': 0, 'toDay': 6, 'toHour': 20, 'toMinute': 0},
            {'fromDay': 1, 'fromHour': 3, 'fromMinute': 0, 'toDay': 4, 'toHour': 6, 'toMinute': 0}
        ]
    }
]

GET_ROLES_RESPONSE = [{
    'Type': 1,
    'Contents': ROLES
}]

SHIFT1_USERS = [
    {
        'Type': 1,
        'Contents': [
            {
                'id': 'user1',
                'name': 'User1'
            },
            {
                'id': 'user2',
                'name': 'User2'
            }
        ]
    }
]

SHIFT2_USERS = [
    {
        'Type': 1,
        'Contents': [
            {
                'id': 'user3',
                'name': 'User2'
            }
        ]
    }
]

ADMIN_USERS = [
    {
        'Type': 1,
        'Contents': [
            {
                'id': 'admin',
                'name': 'Admin'
            }
        ]
    }
]


def execute_command(name, args=None):
    if name == 'getRoles':
        return GET_ROLES_RESPONSE
    elif name == 'getUsers':
        if args['roles'] == 'Shift1':
            return SHIFT1_USERS
        elif args['roles'] == 'Shift2':
            return SHIFT2_USERS
        elif args['roles'] == 'Administrator':
            return ADMIN_USERS
    else:
        return None


def test_get_oncall_hours_per_user(mocker):
    mocker.patch.object(demisto, 'executeCommand', side_effect=execute_command)
    mocker.patch.object(demisto, 'results')
    main()
    results = demisto.results.call_args[0]
    assert len(results) == 1
    assert json.loads(results[0]) == [
        {
            "name": "User1", "data": [128], "groups": [{"name": "User1", "data": [128]}]
        },
        {
            "name": "User2", "data": [331], "groups": [{"name": "User2", "data": [331]}]
        },
        {
            "name": "Admin", "data": [0], "groups": [{"name": "Admin", "data": [0]}]
        }
    ]
