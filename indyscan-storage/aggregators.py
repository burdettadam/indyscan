[#parent child did report
    {
        '$match': {
            'txn.type': '1'
        }
    }, {
        '$group': {
            '_id': '$txn.data.dest', 
            'roles': {
                '$push': '$txn.data.role'
            }, 
            'parent': {
                '$push': '$txn.metadata.from'
            }, 
            'aliases': {
                '$push': '$txn.data.alias'
            }
        }
    }
]

[ # billing
    {
        '$match': {
            'txnMetadata.txnTime': {
                '$gte': 1569888000, 
                '$lt': 1572566400
            }
        }
    }, {
        '$group': {
            '_id': '$txn.metadata.from', 
            'txns': {
                '$push': '$$ROOT'
            }
        }
    }, {
        '$addFields': {
            'nyms': {
                '$filter': {
                    'input': '$txns', 
                    'as': 'i', 
                    'cond': {
                        '$eq': [
                            '$$i.txn.type', '1'
                        ]
                    }
                }
            }, 
            'attribs': {
                '$filter': {
                    'input': '$txns', 
                    'as': 'i', 
                    'cond': {
                        '$eq': [
                            '$$i.txn.type', '100'
                        ]
                    }
                }
            }, 
            'schemas': {
                '$filter': {
                    'input': '$txns', 
                    'as': 'i', 
                    'cond': {
                        '$eq': [
                            '$$i.txn.type', '101'
                        ]
                    }
                }
            }, 
            'cred_defs': {
                '$filter': {
                    'input': '$txns', 
                    'as': 'i', 
                    'cond': {
                        '$eq': [
                            '$$i.txn.type', '102'
                        ]
                    }
                }
            }, 
            'rev_regs': {
                '$filter': {
                    'input': '$txns', 
                    'as': 'i', 
                    'cond': {
                        '$eq': [
                            '$$i.txn.type', '113'
                        ]
                    }
                }
            }, 
            'rev_reg_entrys': {
                '$filter': {
                    'input': '$txns', 
                    'as': 'i', 
                    'cond': {
                        '$eq': [
                            '$$i.txn.type', '114'
                        ]
                    }
                }
            }
        }
    }, {
        '$addFields': {
            'nymsTotal': {
                '$size': '$nyms'
            }, 
            'attribsTotal': {
                '$size': '$attribs'
            }, 
            'schemasTotal': {
                '$size': '$schemas'
            }, 
            'cred_defsTotal': {
                '$size': '$cred_defs'
            }, 
            'rev_regsTotal': {
                '$size': '$rev_regs'
            }, 
            'rev_reg_entrysTotal': {
                '$size': '$rev_reg_entrys'
            }
        }
    }, {
        '$addFields': {
            'children': {
                '$slice': [
                    {
                        '$map': {
                            'input': '$nyms', 
                            'as': 'nymTxn', 
                            'in': [
                                '$$nymTxn.txn.data'
                            ]
                        }
                    }, -1
                ]
            }, 
            'child_did': {
                '$map': {
                    'input': '$nyms', 
                    'as': 'nymTxn', 
                    'in': [
                        '$$nymTxn.txn.data.dest'
                    ]
                }
            }
        }
    }, {
        '$lookup': {
            'from': 'did-roles-parent', 
            'localField': '_id', 
            'foreignField': '_id', 
            'as': 'roles'
        }
    }, {
        '$unwind': {
            'path': '$roles'
        }
    }, {
        '$project': {
            'nymsTotal': 1, 
            'attribsTotal': 1, 
            'schemasTotal': 1, 
            'cred_defsTotal': 1, 
            'rev_regsTotal': 1, 
            'rev_reg_entrysTotal': 1, 
            'role': {
                '$arrayElemAt': [
                    '$roles.roles', -1
                ]
            }
        }
    }
]