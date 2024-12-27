/** @odoo-module */

import { Field } from '@web/views/fields/field';
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { usePopover } from "@web/core/popover/popover_hook";
import { onPartnerSubRedirect } from './hooks';


const { Component, onWillStart, onWillRender, useState } = owl;

function useUniquePopover() {
    const popover = usePopover();
    let remove = null;
    return Object.assign(Object.create(popover), {
        add(target, component, props, options) {
            if (remove) {
                remove();
            }
            remove = popover.add(target, component, props, options);
            return () => {
                remove();
                remove = null;
            };
        },
    });
}

class PartnerOrgChartPopover extends Component {
    async setup() {
        super.setup();

        this.rpc = useService('rpc');
        this.orm = useService('orm');
        this.actionService = useService("action");
        this._onPartnerSubRedirect = onPartnerSubRedirect();
    }

    /**
     * Redirect to the partner form view.
     *
     * @private
     * @param {MouseEvent} event
     * @returns {Promise} action loaded
     */
    async _onPartnerRedirect(partnerId) {
        const action = await this.orm.call('res.partner', 'get_formview_action', [partnerId]);
        this.actionService.doAction(action);
    }

}
PartnerOrgChartPopover.template = 'partner_org_chart.partner_org_chart_popover';

export class PartnerOrgChart extends Field {
    async setup() {
        super.setup();

        this.rpc = useService('rpc');
        this.orm = useService('orm');
        this.actionService = useService("action");
        this.popover = useUniquePopover();

        this.jsonStringify = JSON.stringify;

        this.state = useState({ 'partner_id': null });
        this.lastParent = null;
        this._onPartnerSubRedirect = onPartnerSubRedirect();

        onWillStart(this.handleComponentUpdate.bind(this));
        onWillRender(this.handleComponentUpdate.bind(this));
    }

    async handleComponentUpdate() {
        this.partner = this.props.record.data;
        this.state.partner_id = this.partner.id;
        const manager = this.partner.parent_id;
        const forceReload = this.lastRecord !== this.props.record || this.lastParent !== manager;
        this.lastParent = manager;
        this.lastRecord = this.props.record;
        await this.fetchPartnerData(this.state.partner_id, forceReload);
    }

    async fetchPartnerData(partnerId, force = false) {
        if (!partnerId) {
            this.managers = [];
            this.children = [];
            if (this.view_partner_id) {
                this.render(true);
            }
            this.view_partner_id = null;
        } else if (partnerId !== this.view_partner_id || force) {
            this.view_partner_id = partnerId;
            var orgData = await this.rpc('/partner/get_org_chart',
                {
                partner_id: partnerId,
                context: Component.env.session.user_context,
                }
            );
            this.managers = orgData.managers || [];
            this.children = orgData.children || [];
            this.data = orgData.data;
            this.child_ids = orgData.child_ids || [];
            this.render(true);
        }
    }

    _onOpenPopover(event, partner) {
        this.popover.add(
            event.currentTarget,
            this.constructor.components.Popover,
            { partner },
            { closeOnClickAway: true }
        );
    }

    async _onPartnerMoreManager(managerId) {
        await this.fetchPartnerData(managerId);
        this.state.partner_id = managerId;
    }

    async _onPartnerRedirect(partnerId) {
        const action = await this.orm.call('res.partner', 'get_formview_action', [partnerId]);
        this.actionService.doAction(action);
    }
}

PartnerOrgChart.components = {
    Popover: PartnerOrgChartPopover,
};

PartnerOrgChart.template = 'partner_org_chart.partner_org_chart';

registry.category("fields").add("partner_org_chart", PartnerOrgChart);
