## users 
| Parameter | CREATE required | UPDATE required | ReadOnly |DataType | Description |
|-|-|-|-|-|-|
| id |  | True | True | integer | Automatically assigned when the user is created |
| email |  |  |  | string | The user's primary email address. Writeable on create only. On update, a secondary email is added. |
| name | True |  |  | string | The user's name |
| active |  |  | True | boolean | false if the user has been deleted |
| alias |  |  |  | string | An alias displayed to end users |
| chat_only |  |  | True | boolean | Whether or not the user is a chat-only agent |
| created_at |  |  | True | date | The time the user was created |
| custom_role_id |  |  |  | integer | A custom role if the user is an agent on the Enterprise plan |
| role_type |  |  | True | integer | The user's role id. 0 for custom agents, 1 for light agent, 2 for chat agent, and 3 for chat agent added to the Support account as a contributor |
| details |  |  |  | string | Any details you want to store about the user, such as an address |
| external_id |  |  |  | string | A unique identifier from another system. The API treats the id as case insensitive. Example: ian1 and Ian1 are the same user |
| last_login_at |  |  | True | date | The last time the user signed in to Zendesk Support |
| locale |  |  |  | string | The user's locale. A BCP-47 compliant tag for the locale. If both "locale" and "locale_id" are present on create or update, "locale_id" is ignored and only "locale" is used. |
| locale_id |  |  |  | integer | The user's language identifier |
| moderator |  |  |  | boolean | Designates whether the user has forum moderation capabilities |
| notes |  |  |  | string | Any notes you want to store about the user |
| only_private_comments |  |  |  | boolean | true if the user can only create private comments |
| organization_id |  |  |  | integer | The id of the user's organization. If the user has more than one organization memberships, the id of the user's default organization |
| default_group_id |  |  |  | integer | The id of the user's default group. *Can only be set on create, not on update |
| phone |  |  |  | string | The user's primary phone number. See Phone Number below |
| shared_phone_number |  |  | True | boolean | Whether the phone number is shared or not |
| photo |  |  |  | attachment | NOT SUPPORTED. The user's profile picture represented as an Attachment object |
| restricted_agent |  |  |  | boolean | If the agent has any restrictions; false for admins and unrestricted agents, true for other agents |
| role |  |  |  | string | The user's role. Possible values are "end-user", "agent", or "admin" |
| shared |  |  | True | boolean | If the user is shared from a different Zendesk Support instance. Ticket sharing accounts only |
| shared_agent |  |  | True | boolean | If the user is a shared agent from a different Zendesk Support instance. Ticket sharing accounts only |
| signature |  |  |  | string | The user's signature. Only agents and admins can have signatures |
| suspended |  |  |  | boolean | If the agent is suspended. Tickets from suspended users are also suspended, and these users cannot sign in to the end user portal |
| tags |  |  |  | array | The user's tags. Only present if your account has user tagging enabled |
| ticket_restriction |  |  |  | string | Specifies which tickets the user has access to. Possible values are: "organization", "groups", "assigned", "requested", null |
| time_zone |  |  |  | string | The user's time zone |
| two_factor_auth_enabled |  |  | True | boolean | If two factor authentication is enabled |
| updated_at |  |  | True | date | The time the user was last updated |
| url |  |  | True | string | The user's API url |
| user_fields |  |  |  | object | Values of custom fields in the user's profile. See [User Fields](https://developer.zendesk.com/rest_api/docs/support/users#user-fields) |
| verified |  |  |  | boolean | The user's primary identity is verified or not. For secondary identities, see [User Identities](https://developer.zendesk.com/rest_api/docs/support/user_identities) |
| report_csv |  |  | True | boolean | Whether or not the user can access the CSV report on the Search tab of the Reporting page in the Support admin interface |

## groups 
| Parameter | CREATE required | UPDATE required | ReadOnly |DataType | Description |
|-|-|-|-|-|-|
| id |  | True | True | integer | Automatically assigned when creating groups |
| url |  |  | True | string | The API url of this group |
| name | True |  |  | string | The name of the group |
| description |  |  |  | string | The description of the group |
| default |  |  | True | boolean | If group is default for the account |
| deleted |  |  | True | boolean | Deleted groups get marked as such |
| created_at |  |  | True | date | The time the group was created |
| updated_at |  |  | True | date | The time of the last update of the group |

## organizations 
| Parameter | CREATE required | UPDATE required | ReadOnly |DataType | Description |
|-|-|-|-|-|-|
| id |  | True | True | integer | Automatically assigned when the organization is created |
| url |  |  | True | string | The API url of this organization |
| external_id |  |  |  | string | A unique external id to associate organizations to an external record |
| name | True |  |  | string | A unique name for the organization |
| created_at |  |  | True | date | The time the organization was created |
| updated_at |  |  | True | date | The time of the last update of the organization |
| domain_names |  |  |  | array | An array of domain names associated with this organization |
| details |  |  |  | string | Any details obout the organization, such as the address |
| notes |  |  |  | string | Any notes you have about the organization |
| group_id |  |  |  | integer | New tickets from users in this organization are automatically put in this group |
| shared_tickets |  |  |  | boolean | End users in this organization are able to see each other's tickets |
| shared_comments |  |  |  | boolean | End users in this organization are able to see each other's comments on tickets |
| tags |  |  |  | array | The tags of the organization |
| organization_fields |  |  |  | object | Custom fields for this organization |

## tickets 
| Parameter | CREATE required | UPDATE required | ReadOnly |DataType | Description |
|-|-|-|-|-|-|
| id |  | True | True | integer | Automatically assigned when the ticket is created |
| url |  |  | True | string | The API url of this ticket |
| external_id |  |  |  | string | An id you can use to link Zendesk Support tickets to local records |
| type |  |  |  | string | The type of this ticket. Possible values: "problem", "incident", "question" or "task" |
| subject |  |  |  | string | The value of the subject field for this ticket |
| raw_subject |  |  |  | string | The dynamic content placeholder |
| description |  |  | True | string | Read-only first comment on the ticket |
| comment | True |  |  | object | Description required when creating a ticket. Please refer to [Description and first comment](https://developer.zendesk.com/rest_api/docs/support/tickets#description-and-first-comment) |
| priority |  |  |  | string | The urgency with which the ticket should be addressed. Possible values: "urgent", "high", "normal", "low" |
| status |  |  |  | string | The state of the ticket. Possible values: "new", "open", "pending", "hold", "solved", "closed" |
| recipient |  |  |  | string | The original recipient e-mail address of the ticket |
| requester_id |  |  |  | integer | The user who requested this ticket |
| submitter_id |  |  |  | integer | The user who submitted the ticket. The submitter always becomes the author of the first comment on the ticket |
| assignee_id |  |  |  | integer | The agent currently assigned to the ticket |
| organization_id |  |  |  | integer | The organization of the requester. You can only specify the ID of an organization associated with the requester |
| group_id |  |  |  | integer | The group this ticket is assigned to |
| collaborator_ids |  |  |  | array | The ids of users currently CC'ed on the ticket |
| collaborators |  |  |  | array | POST requests only. Users to add as cc's when creating a ticket. See [Setting Collaborators](https://developer.zendesk.com/rest_api/docs/support/tickets#setting-collaborators) |
| email_cc_ids |  |  |  | array | The ids of agents or end users currently CC'ed on the ticket. See [CCs and followers resources](https://support.zendesk.com/hc/en-us/articles/360020585233) in the Support Help Center |
| follower_ids |  |  |  | array | The ids of agents currently following the ticket. See [CCs and followers resources](https://support.zendesk.com/hc/en-us/articles/360020585233) |
| forum_topic_id |  |  | True | integer | The topic in the Zendesk Web portal this ticket originated from, if any. The Web portal is deprecated |
| problem_id |  |  |  | integer | For tickets of type "incident", the ID of the problem the incident is linked to |
| has_incidents |  |  | True | boolean | Is true if a ticket is a problem type and has one or more incidents linked to it. Otherwise, the value is false |
| due_at |  |  |  | date | If this is a ticket of type "task" it has a due date. Due date format uses ISO 8601 format. |
| tags |  |  |  | array | The array of tags applied to this ticket |
| via |  |  | True | via | This object explains how the ticket was created |
| custom_fields |  |  |  | array | Custom fields for the ticket. See [Setting custom field values](https://developer.zendesk.com/rest_api/docs/support/tickets#setting-custom-field-values) |
| satisfaction_rating |  |  | True | object | The satisfaction rating of the ticket, if it exists, or the state of satisfaction, 'offered' or 'unoffered' |
| sharing_agreement_ids |  |  | True | array | The ids of the sharing agreements used for this ticket |
| followup_ids |  |  | True | array | The ids of the followups created from this ticket. Ids are only visible once the ticket is closed |
| via_followup_source_id |  |  |  | integer | POST requests only. The id of a closed ticket when creating a follow-up ticket. See [Creating Follow-up Tickets](https://developer.zendesk.com/rest_api/docs/support/tickets#creating-follow-up-tickets) |
| macro_ids |  |  |  | array | CREATE requests only. List of macro IDs to be recorded in the ticket audit |
| ticket_form_id |  |  |  | integer | Enterprise only. The id of the ticket form to render for the ticket |
| brand_id |  |  |  | integer | Enterprise only. The id of the brand this ticket is associated with |
| allow_channelback |  |  | True | boolean | Is false if channelback is disabled, true otherwise. Only applicable for channels framework ticket |
| allow_attachments |  |  | True | boolean | When an agent responds, are they allowed to add attachments? Defaults to true |
| is_public |  |  | True | boolean | Is true if any comments are public, false otherwise |
| created_at |  |  | True | date | When this record was created |
| updated_at |  |  | True | date | When this record last got updated |

