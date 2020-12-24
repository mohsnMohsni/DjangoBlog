function likeComment(comment_id, condition) {
    let json_data = JSON.stringify({comment_id, condition});
    $.ajax({
        type: "POST",
        url: "/comment_like/",
        data: json_data,
        success: function (response) {
            let path = window.location.pathname;
            slug = path.match(/[^\/]*/g)[3]
            getComments(`/get_commnets/${slug}/`)
        },
    });
}

function getComments(path) {
    console.log(path)
    $.ajax({
        type: "GET",
        url: path,
        success: function (response) {
            let render_response = "";
            for (let parent of response) {
                render_response += `  
                <div class="card border-primary mb-3 w-75">
                    <div class="card-header">${parent.author}</div>
                    <div class="card-body text-primary">
                      <p class="card-text">${parent.content}</p>
                      <div class="d-flex justify-content-between">
                        <small class="text-muted font-weight-lighter">${parent.create_at}</small>
                        <div class="d-flex justify-content-between" style="width: 20%">
                          <div class="d-flex" style="width: 50px;">
                            <button class="text-muted my_style-btn" style="width: 45px;"
                                    onclick="likeComment(${parent.id}, false)">
                              <img class="my_style-img"
                                   src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAABP0lEQVRIid3Uu0pDQRSF4Q/sbdTgBdGAgp2CYGUhiZY+g0/gq1hZiYWFtW3ewsIIBrVQFMSAFsYYQTQWJ8FDmHNJgoUumGZmzfrZezbDf9IcKpj6LUAFbVRR6Oxt4hpHWIp5izjAHT5wj0MspAEKqAUgW3jrBO1iB+8dX+9qYjsJMI2nmDkEaeMrITwOWQwB9gLmJEjWOgoBagnmXkgzB6AeAjynXIhDNvCaAfjESC+gmnHpws8Ir6OR4r0NVbCfo/S8lRyHAMuyJ6SN8xyQ9RCA6PXzTElau06SwmFM1L88kHglZdEI1zGTBoA16Q+YBNlCKSu8qxJaOSHxdvWlbcl/TlolfamMl5TgFq6GhaziMRDeEPV9AmeGbFcRl7HwB6zEzruQG8wPAoBJnIo+xVBIAbODhnc1ivFhQ/6WvgEV/OIklDEUsQAAAABJRU5ErkJggg=="
                                   alt=""/>
                              ${parent.dislike_count}
                            </button>
                            <button class="text-muted my_style-btn" style="width: 45px;"
                                    onclick="likeComment(${parent.id}, true)">
                              <img class="my_style-img"
                                   src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAA/klEQVRIie3VPUrEUBiF4UcLLSxkQBD8BXEXgqWNaxAXIO5CN6C9zBJEsFErsdBC0EZQFEewsxEcqym08AZCvPmbpJwXPgiXc99DvhRhRAljOeeL2MAM3nGKz0ymg03M4wNnIVvIJA4xwE9q+thJ5XbDWTozwAEm8uTjOMlcys4e9ksyx8H1j+2Si3VmK1Zw1WLBZawgu9Mm85VI07v6jrUOST9WcNNiQdS1pr0Vrec1d1uQHxW92hTuG8jvgqOQOfSGkPfC3Uos46WG/A2rVeUJS3iuIH/FSl15wgKeCuSPIdOIWfEP/6DGzsvo4Dolv/X3r2iVaVzgPDyPaIdf3gzJzXRN+VAAAAAASUVORK5CYII="
                                   alt=""/>
                              ${parent.like_count}
                            </button>
                          </div>
                          <a class="text-decoration-none text-muted"
                             href="{% url 'blog:post' post.slug %}?parent={{ comment.0.id }}#comment">
                            Reply</a>
                        </div>
                      </div>
                    </div>
                  </div>`;
                for (let child of parent.children) {
                    render_response += `
                    <div class="d-flex align-items-end flex-column w-75">
                      <div class="card border-primary mb-2" style="width: 85%;">
                        <div class="card-header d-flex justify-content-between">
                          <span>${child.author}</span>
                          <span>replied to: @${parent.author}</span>
                        </div>
                        <div class="card-body text-primary">
                          <p class="card-text">${child.content}</p>
                          <div class="d-flex justify-content-between">
                            <small class="text-muted font-weight-lighter">${child.create_at}</small>
                            <div class="d-flex" style="width: 15%;">
                              <button class="text-muted my_style-btn"
                                      onclick="likeComment(${child.id}, false)">
                                <img class="my_style-img"
                                     src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAABP0lEQVRIid3Uu0pDQRSF4Q/sbdTgBdGAgp2CYGUhiZY+g0/gq1hZiYWFtW3ewsIIBrVQFMSAFsYYQTQWJ8FDmHNJgoUumGZmzfrZezbDf9IcKpj6LUAFbVRR6Oxt4hpHWIp5izjAHT5wj0MspAEKqAUgW3jrBO1iB+8dX+9qYjsJMI2nmDkEaeMrITwOWQwB9gLmJEjWOgoBagnmXkgzB6AeAjynXIhDNvCaAfjESC+gmnHpws8Ir6OR4r0NVbCfo/S8lRyHAMuyJ6SN8xyQ9RCA6PXzTElau06SwmFM1L88kHglZdEI1zGTBoA16Q+YBNlCKSu8qxJaOSHxdvWlbcl/TlolfamMl5TgFq6GhaziMRDeEPV9AmeGbFcRl7HwB6zEzruQG8wPAoBJnIo+xVBIAbODhnc1ivFhQ/6WvgEV/OIklDEUsQAAAABJRU5ErkJggg=="
                                     alt=""/>
                                ${child.dislike_count}
                              </button>
                              <button class="text-muted my_style-btn"
                                      onclick="likeComment(${child.id}, true)">
                                <img class="my_style-img"
                                     src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAA/klEQVRIie3VPUrEUBiF4UcLLSxkQBD8BXEXgqWNaxAXIO5CN6C9zBJEsFErsdBC0EZQFEewsxEcqym08AZCvPmbpJwXPgiXc99DvhRhRAljOeeL2MAM3nGKz0ymg03M4wNnIVvIJA4xwE9q+thJ5XbDWTozwAEm8uTjOMlcys4e9ksyx8H1j+2Si3VmK1Zw1WLBZawgu9Mm85VI07v6jrUOST9WcNNiQdS1pr0Vrec1d1uQHxW92hTuG8jvgqOQOfSGkPfC3Uos46WG/A2rVeUJS3iuIH/FSl15wgKeCuSPIdOIWfEP/6DGzsvo4Dolv/X3r2iVaVzgPDyPaIdf3gzJzXRN+VAAAAAASUVORK5CYII="
                                     alt=""/>
                                ${child.like_count}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                  </div>`;
                }
            }
            $("#comments").html(render_response);
        },
    });
}
