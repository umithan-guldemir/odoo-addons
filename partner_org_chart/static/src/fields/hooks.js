/** @odoo-module */

import session from 'web.session'
import { useService } from "@web/core/utils/hooks";
import { useEnv } from "@odoo/owl";

/**
 * Redirect to the sub partner kanban view.
 *
 * @private
 * @param {MouseEvent} event
 * @returns {Promise} action loaded
 *
 */
export function onPartnerSubRedirect() {
    const actionService = useService('action');
    const orm = useService('orm');
    const env = useEnv();

    return async (event) => {
        const partnerId = parseInt(event.currentTarget?.dataset.partnerId); // Use optional chaining to avoid errors
        if (!partnerId) {
            console.warn('Partner ID is missing or invalid');
            return;
        }
        const type = event.currentTarget.dataset.type || 'direct';

        try {
            // Fetch action data for the partner
            let action = await orm.call('res.partner', 'get_formview_action', [partnerId]);
            action = {
                ...action,
                name: env._t('Team'),
                view_mode: 'kanban,list,form',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form']],
                domain: [['id', 'in', partnerId]],
                res_id: false,
                context: {
                    default_parent_id: partnerId,
                },
            };
            await actionService.doAction(action);
        } catch (error) {
            console.error('Failed to redirect:', error);
        }
    };
}

